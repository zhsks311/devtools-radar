"""Keep storefront geography separate from evidence-backed delivery/activation countries."""
from datetime import date
from tools.validate_data import is_safe_url

# ISO 3166-1 alpha-2. In particular GLOBAL, EU, UK and language codes are not countries.
COUNTRY_CODES = frozenset('AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW'.split())
CONFIRMED_STATUSES = {'retailer_delivery_statement', 'verified_delivery', 'verified_activation'}


def _evidence_errors(info):
    errors = []
    if info.get('status') not in CONFIRMED_STATUSES:
        errors.append('confirmed countries require a reviewed delivery or activation status')
    if not is_safe_url(info.get('evidence_url')):
        errors.append('confirmed countries require a safe evidence URL')
    try:
        value = info.get('checked_at')
        if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value or date.fromisoformat(value) > date.today():
            raise ValueError()
    except (TypeError, ValueError):
        errors.append('confirmed countries require a real non-future YYYY-MM-DD check date')
    field = 'activation' if info.get('status') == 'verified_activation' else 'delivery'
    if not isinstance(info.get(field), str) or not info[field].strip():
        errors.append('confirmed countries require observed delivery/activation evidence')
    return errors


def confirmed_countries(deal):
    """Fail closed; never infer eligibility from currency, language, retailer or region."""
    info = deal.get('purchase_eligibility') or {}
    if not isinstance(info, dict):
        return ()
    codes = info.get('countries_confirmed', [])
    if not isinstance(codes, list) or not codes or any(not isinstance(c, str) or c not in COUNTRY_CODES for c in codes) or _evidence_errors(info):
        return ()
    return tuple(sorted(set(codes)))


def storefront_country(deal):
    # Explicit editorial classification, not a destination or company headquarters.
    code = deal.get('storefront_country')
    return code if isinstance(code, str) and code in COUNTRY_CODES else 'unknown'


def validate_deal_countries(feed):
    errors = []
    for deal in feed:
        prefix = str(deal.get('id', '?')) + ': '
        code = deal.get('storefront_country')
        if code is not None and (not isinstance(code, str) or code not in COUNTRY_CODES):
            errors.append(prefix + 'storefront_country must be an ISO country code or null')
        info = deal.get('purchase_eligibility')
        if info is None:
            continue
        if not isinstance(info, dict):
            errors.append(prefix + 'purchase_eligibility must be an object')
            continue
        codes = info.get('countries_confirmed', [])
        if not isinstance(codes, list) or any(not isinstance(c, str) or c not in COUNTRY_CODES for c in codes):
            errors.append(prefix + 'countries_confirmed must contain ISO country codes')
        elif codes:
            errors.extend(prefix + error for error in _evidence_errors(info))
    return errors
