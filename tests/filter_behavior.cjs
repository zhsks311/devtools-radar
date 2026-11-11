// Execute the production filter code, not a reimplementation. No npm dependencies.
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {js, pages} = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
let combinations = 0;
for (const page of pages) {
  const nodes = {}, events = {};
  for (const [id, values] of Object.entries(page.selects)) {
    nodes['#'+id] = {value:'all', options:values.map(value=>({value})),
      addEventListener(type, listener){this[type]=listener}, focus(){this.focused=true}};
  }
  for (const id of ['count','archive-count','empty','reset-filters']) {
    nodes['#'+id] = {hidden:false, dataset:{label:'products'}, addEventListener(type, fn){this[type]=fn}};
  }
  nodes['.held-archive'] = {hidden:false};
  const cards = page.cards.map(dataset=>({dataset, hidden:false}));
  const archived = page.archived.map(dataset=>({dataset, hidden:false}));
  const links = page.links.map(href=>({href:'https://example.test'+href}));
  let url = new URL('https://example.test/deals/?country=INVALID&market=INVALID&category=INVALID&utm_source=test#keep');
  const location = {};
  for(const key of ['search','pathname','hash']) Object.defineProperty(location,key,{get:()=>url[key]});
  const context = vm.createContext({URLSearchParams, URL, location,
    history:{replaceState(a,b,value){url=new URL(value,url)}},
    document:{querySelector:selector=>nodes[selector], querySelectorAll(selector){
      return selector==='#active-products .card'?cards:selector==='#held-products .card'?archived:links.map(a=>({
        get href(){return new URL(a.href,url).href}, set href(v){a.href=v}
      }));}},
    window:{addEventListener(type,fn){events[type]=fn}}
  });
  vm.runInContext(js, context);
  assert.equal(nodes['#country'].value,'all');
  assert.equal(url.search,'?utm_source=test'); assert.equal(url.hash,'#keep');
  for(const market of page.selects.market) for(const country of page.selects.country) for(const category of page.selects.category) {
    nodes['#market'].value=market; nodes['#country'].value=country; nodes['#category'].value=category;
    nodes['#country'].change();
    const matches = d => (market==='all'||d.market===market) && (category==='all'||d.category===category) &&
      (country==='all'||(country==='unknown'?d.countries==='':d.countries.split(' ').includes(country)));
    const expected=page.cards.filter(matches).map(d=>d.id), held=page.archived.filter(matches).map(d=>d.id);
    assert.deepEqual(cards.filter(d=>!d.hidden).map(d=>d.dataset.id),expected);
    assert.deepEqual(archived.filter(d=>!d.hidden).map(d=>d.dataset.id),held);
    assert.equal(nodes['#count'].textContent,expected.length+' products');
    assert.equal(nodes['#archive-count'].textContent,held.length);
    assert.equal(nodes['#empty'].hidden,expected.length>0);
    assert.equal(nodes['.held-archive'].hidden,held.length===0);
    for(const key of ['market','country','category']) {
      const val=nodes['#'+key].value;
      assert.equal(url.searchParams.get(key),val==='all'?null:val);
      for(const link of links) assert.equal(new URL(link.href,url).searchParams.get(key),val==='all'?null:val);
    }
    combinations++;
  }
  nodes['#reset-filters'].click();
  assert.equal(nodes['#reset-filters'].hidden,true);
  assert.equal(nodes['#count'].textContent,'13 products');
  assert.equal(url.search,'?utm_source=test'); assert.equal(url.hash,'#keep');
  url=new URL('https://example.test/deals/?market=CN&category=keyboard-mouse&country=unknown'); events.popstate();
  assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.id),['lenovo-gk10-rt60-cn']);
  url=new URL('https://example.test/deals/?country=AU'); events.pageshow();
  assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.id),['43ca41d03daa']);
  // Matching uses country membership, not a single country equality check.
  cards[0].dataset.countries='AU NZ';
  nodes['#country'].options.push({value:'NZ'});
  url=new URL('https://example.test/deals/?country=NZ'); events.popstate();
  assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.id),[cards[0].dataset.id]);
}
console.log(combinations+' filter combinations passed; invalid URLs, reset, language links, history, restore and multi-country checked.');
