import streamlit as st
from datetime import date, timedelta

from st_rsuite import date_picker, date_range_picker

disabled = st.session_state.get("disabled", False)

st.markdown(
    "All st-rsuite components accept a `locale` parameter that switches "
    "calendar labels, month/day names, and button text to the target language. "
    "RSuite ships 29 locales out of the box."
)

_LOCALES = [
    ("Japanese", "ja_JP"),
    ("Chinese (Simplified)", "zh_CN"),
    ("Spanish", "es_ES"),
    ("Korean", "ko_KR"),
    ("Arabic", "ar_EG"),
    ("French", "fr_FR"),
]

st.markdown("#### DatePicker (one-tap)")

cols = st.columns(3)
for i, (lang, code) in enumerate(_LOCALES):
    with cols[i % 3]:
        dp_loc = date_picker(
            label=f"{lang} ({code})",
            value=date.today(),
            one_tap=True,
            locale=code,
            disabled=disabled,
            key=f"dp_locale_{code}",
        )
        st.code(f"{dp_loc}")

st.divider()

st.markdown("#### DateRangePicker")

cols2 = st.columns(3)
for i, (lang, code) in enumerate(_LOCALES):
    with cols2[i % 3]:
        drp_loc = date_range_picker(
            label=f"{lang} ({code})",
            value=(date.today(), date.today() + timedelta(days=7)),
            locale=code,
            disabled=disabled,
            key=f"drp_locale_{code}",
        )
        st.code(f"{drp_loc[0]} ~ {drp_loc[1]}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        '''from st_rsuite import date_picker, date_range_picker
from datetime import date

# Japanese locale
selected = date_picker(
    label="Pick a date",
    value=date.today(),
    locale="ja_JP",
    one_tap=True,
    key="my_jp_date",
)

# Available locales:
# ar_EG, ca_ES, cs_CZ, da_DK, de_DE, en_GB, en_US,
# es_AR, es_ES, fa_IR, fi_FI, fr_FR, gu_IN, hu_HU,
# it_IT, ja_JP, kk_KZ, ko_KR, ne_NP, nl_NL, pl_PL,
# pt_BR, ru_RU, sv_SE, th_TH, tr_TR, uk_UA, zh_CN, zh_TW''',
        language="python",
    )
