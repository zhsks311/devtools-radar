"""Small source-backed buying guides, not invented hands-on reviews."""
from html import escape as e
import datetime
from tools.deal_prices import current_price_state, number
from tools.deal_availability import explicit_offer_expiry
from tools.product_links import publishable_link
from pathlib import Path

PATHS={'en':'/guides/screen-recording/','ko':'/guides/ko/screen-recording/'}
TITLES={'en':'OBS or Action! for screen recording? Compare cost and license rights','ko':'화면 녹화 도구 고르기: 무료 OBS와 Action! 가격·사용권 비교'}
LABELS={'en':'Screen recording buying guide','ko':'화면 녹화 구매 가이드','zh':'屏幕录制购买指南（英文）','ja':'画面録画の購入ガイド（英語）','es':'Guía de grabación de pantalla (inglés)','fr':'Guide d’enregistrement vidéo (anglais)'}
OBS='https://obsproject.com/'
FAQ='https://mirillis.com/purchase-faq'
OFFICIAL='https://mirillis.com/store-action-paysafecard'

def current_reseller_offer(deal, now):
    if not deal or deal.get('currency') != 'USD' or not publishable_link(deal):
        return None
    expiry = explicit_offer_expiry(deal.get('expires_at'))
    if (expiry is not None and now >= expiry) or (deal.get('availability_review') or {}).get('status') in {'expired', 'sold_out'}:
        return None
    if current_price_state(deal, now=now) != 'observed':
        return None
    return deal

def guide(lang, deal=None, *, now=None):
    now = now or datetime.datetime.now(datetime.timezone.utc)
    ko = lang == 'ko'
    title = TITLES[lang]
    catalog = '/ko/' if ko else '/deals/'
    link = lambda url, label: f'<a href="{e(url)}" rel="noopener nofollow">{e(label)}</a>'
    deal = current_reseller_offer(deal, now)
    reseller = ''
    offer_reference = ''
    if deal:
        price = f"USD {number(deal['price']):.2f}"
        seller = deal['link']['url']
        stamp = deal['price_review']['review_completed_at']
        if ko:
            reseller = f"<dt>StackSocial · {price}</dt><dd>신규 사용자용 Windows 1대 라이선스입니다. 상업 이용권은 확인되지 않았습니다. 등록 기한과 환불 조건을 판매처에서 확인하세요. {link(seller, 'StackSocial 상품·조건 확인')}</dd>"
        else:
            reseller = f"<dt>StackSocial · {price}</dt><dd>For new users on one Windows device. Commercial use has not been confirmed. See the seller for redemption and refund terms. {link(seller, 'StackSocial product and terms')}</dd>"
        checked = '판매처 표시가 확인' if ko else 'Seller price checked'
        back = '상품 카드로 돌아가기' if ko else 'Return to product card'
        offer_reference = f'<p>{checked}: <time datetime="{e(stamp)}">{e(stamp)}</time></p><p><a href="{catalog}#product-{e(deal["id"])}">{back}</a></p>'
    if ko:
        desc='무료 녹화 도구와 유료 라이선스의 차이, 신규 사용자 제한, 상업 이용과 환불 조건을 구매 전에 확인하세요.'
        body=f'''<p>단순히 가장 싼 녹화 프로그램을 찾기보다, 무료 도구로 충분한지와 만든 영상으로 수익을 낼지부터 구분하세요. 이 글은 공식 문서·판매처 조건을 비교한 구매 가이드이며 직접 사용한 성능 리뷰가 아닙니다.</p>
<h2>먼저 고를 경로</h2><ul><li><strong>비용 없이 녹화·방송 시작:</strong> OBS Studio부터 검토하세요. 무료 오픈소스이며 Windows·macOS·Linux를 지원합니다. 장면과 여러 영상·음성 소스를 구성할 수 있습니다. {link(OBS,'OBS 공식 기능·다운로드')}</li><li><strong>Action!이 필요한 Windows 사용자:</strong> 먼저 공식 무료 체험판으로 자신의 게임·마이크·시스템 소리 녹화를 확인하세요. 기능이 충분한지 확인한 뒤 사용권을 고르는 편이 낫습니다.</li><li><strong>유튜브·업무 등 수익 활동:</strong> Home과 Commercial은 다릅니다. 싼 판매처 상품도 상업권이 확인되지 않았다면 수익용으로 추천하지 않습니다.</li></ul>
<h2>Action! 구매 경로와 차이</h2><dl>{reseller}<dt>Mirillis Home</dt><dd>개인 비상업용입니다. 구매 전 공식 가격과 사용권을 확인하세요.</dd><dt>Mirillis Commercial</dt><dd>공식 FAQ는 기업·유튜버 등 수익을 내는 프로젝트용으로 설명합니다. {link(FAQ,'공식 사용권 구분')} · {link(OFFICIAL,'공식 가격과 옵션 확인')}</dd></dl>
<p>공식 결제 페이지에서 다운로드·시리얼 알림 같은 부가서비스의 선택 여부와 비용을 확인하세요. 표시가격은 최종 결제금액 보장이 아니며 한국 구매·활성화, 세금, 결제수단은 확인하지 않았습니다. 서로 다른 사용권 가격을 할인율로 계산하지 않습니다.</p>
<h2>돈을 쓰기 전 확인할 세 가지</h2><ol><li>필요한 화면·게임을 짧게 녹화하고 마이크와 시스템 소리가 모두 들리는지 확인하세요.</li><li>판매처의 신규 사용자·기기 수·상업권 조건이 자신에게 맞는지 확인하세요. 불명확하면 등록 전에 판매처에 문의하세요.</li><li>등록 후 환불이 막히는 조건을 확인하고, 선택 부가서비스와 세금을 포함한 최종금액을 비교하세요.</li></ol>
<h2>확인 범위</h2><p>OBS 기능은 공식 홈페이지, Action! 사용권 구분은 공식 FAQ를 근거로 했습니다. 직접 녹화 성능·고객 평점·최저가·한국 활성화를 검증한 것은 아닙니다. 현재 링크에는 DevTeardown 제휴 추적이 없습니다.</p>'''
    else:
        desc='Compare free OBS with Action! purchase routes, commercial rights, new-user restrictions and refund conditions before paying.'
        body=f'''<p>Start with whether a free recorder meets your needs and whether your recordings will earn money. This is a source-based buying guide, not a hands-on performance review.</p>
<h2>Choose a path first</h2><ul><li><strong>Record or stream without paying:</strong> consider OBS Studio first. It is free and open source on Windows, macOS and Linux, with scenes and multiple video/audio sources. {link(OBS,'Official OBS features and downloads')}</li><li><strong>Need Action! on Windows:</strong> try the official trial with your own game, microphone and system audio before purchasing a license.</li><li><strong>Revenue-producing video or business work:</strong> Home and Commercial rights differ. We do not recommend an unspecified commercial license simply because its price is lower.</li></ul>
<h2>Action! purchase routes</h2><dl>{reseller}<dt>Mirillis Home</dt><dd>Private, non-commercial use. Check the current official price and license terms before buying.</dd><dt>Mirillis Commercial</dt><dd>The official FAQ describes this for organizations, YouTubers and revenue-producing projects. {link(FAQ,'Official license distinctions')} · {link(OFFICIAL,'Official prices and options')}</dd></dl>
<p>Check the official checkout for optional services and their fees. Base prices are not guaranteed final bills. Taxes, payment-country eligibility and activation in Korea are unverified. Different license scopes are not treated as a like-for-like discount.</p>
<h2>Three checks before spending</h2><ol><li>Make a short recording of your intended screen or game; check microphone and system audio.</li><li>Check new-user, device-count and commercial-use restrictions. Ask the seller before redemption if the terms are unclear.</li><li>Check when refunds stop and compare the final bill including optional services and taxes.</li></ol>
<h2>Evidence and limits</h2><p>OBS features come from its official homepage; Action! license distinctions come from the official FAQ. We have not tested recording performance, customer ratings, historical lows or country activation. These links do not contain DevTeardown affiliate tracking.</p>'''
    languages=' · '.join(f'<a href="{p}" lang="{l}">{"한국어" if l=="ko" else "English"}</a>' for l,p in PATHS.items())
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | DevTeardown</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="https://devteardown.com{PATHS[lang]}"><style>body{{margin:0;background:#fafafa;color:#17202a;font:18px/1.7 system-ui,sans-serif}}main,header{{max-width:760px;margin:auto;padding:24px}}a{{color:#075caf}}h1{{font-size:clamp(27px,5vw,40px);line-height:1.25}}h2{{margin-top:2em}}dt{{font-weight:700;margin-top:20px}}dd{{margin:8px 0 24px;padding-left:16px;border-left:3px solid #bed2e7}}li{{margin-bottom:12px}}time{{overflow-wrap:anywhere}}</style></head><body><header><a href="{catalog}">DevTeardown</a> · {languages}</header><main><h1>{e(title)}</h1>{body}{offer_reference}</main></body></html>'''

def write_guides(output, feeds, *, now=None):
    deal=next((d for d in feeds if d['id']=='0deb259ecfd4'), None)
    now = now or datetime.datetime.now(datetime.timezone.utc)
    for lang,path in PATHS.items():
        target=Path(output)/path.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(guide(lang, deal, now=now), encoding='utf-8')
    return list(PATHS.values())
