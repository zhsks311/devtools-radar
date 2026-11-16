"""Original editorial illustrations, not vendor logos or product screenshots."""
from html import escape
CAPTION = {'ko':'서비스·제품 이해를 돕는 일러스트','en':'Illustration · not a product screenshot','zh':'功能示意图 · 非产品截图','ja':'機能イメージ・実際の製品画面ではありません','es':'Ilustración · no es una captura del producto','fr':'Illustration · pas une capture du produit'}
def illustration(deal,lang):
    ident=deal.get('id',''); category=deal.get('category','software')
    # Simple diagrams explain the category without fabricating a branded UI.
    if 'otter' in ident:
        art='<rect x="60" y="40" width="100" height="110" rx="8"/><rect x="200" y="40" width="100" height="110" rx="8"/><path d="M80 70h60M80 90h40M220 70h60M220 90h40"/><rect class="accent" x="80" y="112" width="60" height="18" rx="4"/><rect class="accent" x="220" y="112" width="40" height="18" rx="4"/><text x="110" y="177">A</text><text x="250" y="177">B</text>'
    elif any(x in ident for x in ('koofr','drive','backup','hostinger','nocode')):
        art='<path d="M100 90V55h60l18 18h82v85H100z"/><path d="M82 90h196l-18 68H100z"/><path class="accent" d="M165 119l15-15 15 15M180 105v38"/>'
    elif 'mail' in ident:
        art='<rect x="80" y="55" width="200" height="110" rx="10"/><path d="M82 60l98 70 98-70M82 160l65-55M278 160l-65-55"/>'
    elif any(x in ident for x in ('guard','pass')):
        art='<path d="M180 35l75 28v51c0 40-75 70-75 70s-75-30-75-70V63z"/><path class="accent" d="M145 105l25 25 47-52"/>'
    elif category=='gaming':
        art='<path d="M112 65h136c18 0 32 70 24 88-8 20-30-8-44-21h-96c-14 13-36 41-44 21-8-18 6-88 24-88z"/><path d="M115 100h38M134 81v38"/><circle class="accent" cx="229" cy="92" r="7"/><circle class="accent" cx="247" cy="111" r="7"/>'
    elif category in ('vouchers','snacks','afterwork'):
        art='<path d="M70 55h220v40a20 20 0 0 0 0 40v35H70v-35a20 20 0 0 0 0-40z"/><path stroke-dasharray="6 8" d="M220 65v95"/><path class="accent" d="M120 110h55M148 83v55"/>'
    elif category in ('hardware','tech','keyboard-mouse','monitor-desk','laptops'):
        art='<rect x="95" y="35" width="170" height="115" rx="9"/><path d="M150 180h60M180 150v30"/><path class="accent" d="M182 55l-25 45h25l-8 30 30-48h-27z"/>'
    else:
        art='<rect x="75" y="35" width="210" height="140" rx="10"/><path d="M75 65h210M95 50h5m10 0h5m10 0h5"/><rect class="accent" x="100" y="90" width="55" height="55" rx="7"/><path d="M175 95h85M175 115h65M175 135h75"/>'
    return '<figure class="editorial-visual"><svg viewBox="0 0 360 210" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'+art+'</g></svg><figcaption>'+escape(CAPTION[lang])+'</figcaption></figure>'
