import streamlit as st
import pandas as pd
import zipfile
import os
import tempfile
import io
import re

st.set_page_config(page_title="TextDigit", layout="wide")

header_cols = st.columns([1,3])
with header_cols[0]:
    st.image("https://khandirect.com/wp-content/uploads/2025/08/new-textedit-logo.png", width=200)
with header_cols[1]:
    st.title("Simple Solution For Complex Data!")

# --- Upload Section ---
st.markdown("### \U0001F4D6 Open Source - Get The Information You Need! Safe, Reliable & Quick!")
st.markdown("""
    <hr style="border:none;height:1px;background-color:#eee;margin:0.5rem 0 0.5rem 0"/>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Drop ZIP or CSV files here",
    type=["csv", "zip"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# --- Instructions if no files uploaded ---
if not uploaded_files:
    st.info("ℹ️ Upload CSV or ZIP files to begin.")
    st.markdown("""
    ### \U0001F527 What You Can Do:
    - \U0001F4C4 **Upload** one or more CSV files, or a ZIP file containing multiple CSVs  
    - \U0001F50E **Search through hundreds of files** simultaneously.
    - \U0001F4BD **Great for large datasets** handling right up to size 200MB files  
    - \U0001F4CB **Apply light to heavy filters** up to the first 10 columns  
    - \u2B07 **Download results instantly** once matched
    - \U0001F4BE **ZIP and CSV** can be uploaded together.
    - \U0001F440 **Apply custom regular expressions** done per filter value

     ### \U0001F3C6 Who Can Use This:
    - \U0001F4B0 **eCommerce sellers** (Amazon, Shopify): filter product/sales data  
    - \U0001F393 **Researchers/academics** clean/filter CSVs for studies  
    - \U0001F3AF **Marketers** filter campaign data, leads, or tracking results  
    - \U0001F9E0 **Data analysts/freelancers** quick filtering/cleaning before analysis               
    - \U0001F4B9 **Financial traders** filter large market data files 
                
    ### \U0001F525 Supported:
    - \u26A1 ZIP with multiple CSVs  
    - \U0001F4C4 Individual CSVs  
    - \U0001F503 With or without headers
   
    ### \U0001F6E1 Additional Information:
    - \U0001F9F2 Pro version go to TextDigit.com      
    - \U0001F680 Bespoke version contact: Ali Khan  
    - \U0001F4E7 alikhan111@gmail.com  
    
    """)

# --- File Extraction ---
all_files = []

if uploaded_files:
    with tempfile.TemporaryDirectory() as tmpdir:
        for uploaded in uploaded_files:
            if uploaded.name.endswith(".zip"):
                try:
                    with zipfile.ZipFile(uploaded, 'r') as zip_ref:
                        zip_ref.extractall(tmpdir)
                        for filename in os.listdir(tmpdir):
                            if filename.endswith(".csv"):
                                filepath = os.path.join(tmpdir, filename)
                                with open(filepath, 'rb') as f:
                                    content = f.read()
                                    all_files.append((filename, content))
                except zipfile.BadZipFile:
                    st.error(f"❌ {uploaded.name} is not a valid ZIP file.")
            elif uploaded.name.endswith(".csv"):
                content = uploaded.read()
                all_files.append((uploaded.name, content))

if all_files:
    has_header = st.checkbox("CSV files have a header row?", value=True)
    match_type = st.radio(
        "Match type:",
        ["Exact Match", "Contains Match (case-insensitive)"]
    )
    regex_mode = st.checkbox("Enable Regex Filtering (Advanced Users)", value=False)

    # Validate that all headers match
    header_set = set()
    for name, content in all_files:
        try:
            file = io.StringIO(content.decode('utf-8', errors='ignore'))
            df = pd.read_csv(file) if has_header else pd.read_csv(file, header=None)
            if not has_header:
                df.columns = [f"Column {i+1}" for i in range(df.shape[1])]
            header_set.add(tuple(df.columns))
        except Exception as e:
            st.error(f"Error reading file {name}: {e}")
            st.stop()

    if len(header_set) > 1:
        st.error("❌ CSV files do not have matching headers. Please ensure all uploaded files share the same column structure.")
        st.stop()

    column_names = list(header_set.pop())

    if 'filters' not in st.session_state:
        st.session_state.filters = []

    def add_filter(index=None):
        new_filter = {'col': None, 'val': ''}
        if index is None:
            st.session_state.filters.append(new_filter)
        else:
            st.session_state.filters.insert(index, new_filter)

    def remove_filter(index):
        if 0 <= index < len(st.session_state.filters):
            st.session_state.filters.pop(index)
            st.rerun()

    if not st.session_state.filters:
        add_filter()

    with st.expander("🔍 Filter Criteria"):
        for i, f in enumerate(st.session_state.filters):
            cols = st.columns([3.5, 3.5, 0.7, 0.7, 0.7])
            selected_col = cols[0].selectbox("", column_names, index=column_names.index(f['col']) if f['col'] in column_names else 0, key=f"col_{i}", label_visibility="collapsed")
            input_val = cols[1].text_input("", value=f['val'], key=f"val_{i}", label_visibility="collapsed")

            if cols[2].button("⬆️", key=f"up_{i}") and i > 0:
                st.session_state.filters[i - 1], st.session_state.filters[i] = st.session_state.filters[i], st.session_state.filters[i - 1]
                st.rerun()

            if cols[3].button("⬇️", key=f"down_{i}") and i < len(st.session_state.filters) - 1:
                st.session_state.filters[i + 1], st.session_state.filters[i] = st.session_state.filters[i], st.session_state.filters[i + 1]
                st.rerun()

            if cols[4].button("❌", key=f"remove_{i}"):
                remove_filter(i)

            st.session_state.filters[i]['col'] = selected_col
            st.session_state.filters[i]['val'] = input_val

        st.markdown("---")
        if st.button("➕ Add Filter"):
            add_filter()
            st.rerun()

    def read_and_filter_csv(file_bytes, filters, has_header, match_type, regex_mode):
        try:
            file = io.StringIO(file_bytes.decode('utf-8', errors='ignore'))
            df = pd.read_csv(file) if has_header else pd.read_csv(file, header=None)
            if not has_header:
                df.columns = [f"Column {i+1}" for i in range(df.shape[1])]
            original_count = len(df)

            for f in filters:
                col_name = f['col']
                val = f['val']
                if col_name in df.columns and val:
                    series = df[col_name].astype(str)

                    if match_type == "Exact Match":
                        if '*' in val:
                            regex_pattern = '^' + re.escape(val).replace('\\*', '.*') + '$'
                            try:
                                df = df[series.str.contains(regex_pattern, case=False, na=False, regex=True)]
                            except re.error:
                                st.warning(f"⚠️ Invalid wildcard pattern in: {val}")
                        elif regex_mode:
                            try:
                                df = df[series.str.contains(val, case=False, na=False, regex=True)]
                            except re.error:
                                st.warning(f"⚠️ Invalid regex: {val}")
                        else:
                            df = df[series.str.strip() == val.strip()]

                    elif match_type == "Contains Match (case-insensitive)":
                        if val.startswith('[') and val.endswith(']'):
                            exact_val = val[1:-1].strip()
                            df = df[series.str.strip() == exact_val]
                        elif regex_mode:
                            try:
                                df = df[series.str.contains(val, case=False, na=False, regex=True)]
                            except re.error:
                                st.warning(f"⚠️ Invalid regex: {val}")
                        else:
                            df = df[series.str.contains(val, case=False, na=False)]

            match_count = len(df)
            return df, original_count, match_count
        except Exception as e:
            st.error(f"Error processing file: {e}")
            return pd.DataFrame(), 0, 0

    def process_files(file_list, filters, has_header, match_type, regex_mode):
        total_entries = 0
        total_matches = 0
        all_filtered = []

        for name, content in file_list:
            df, total, match = read_and_filter_csv(content, filters, has_header, match_type, regex_mode)
            if not df.empty:
                all_filtered.append(df)
            total_entries += total
            total_matches += match

        return all_filtered, total_entries, total_matches

    if any(f['val'] for f in st.session_state.filters):
        filtered_data, total, matched = process_files(all_files, st.session_state.filters, has_header, match_type, regex_mode)

        if filtered_data:
            result_df = pd.concat(filtered_data, ignore_index=True)
            st.success(f"✅ Total Rows Scanned: {total} | Matches Found: {matched}")

            st.markdown("### 📊 Filtered Results Preview (First 5 Rows):")
            st.dataframe(result_df.head(5), use_container_width=True)
            st.caption("⚠️ Full filtered data is available in the download.")

            csv_output = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("📅 Download Full Filtered CSV", csv_output, file_name="filtered_output.csv")
        else:
            st.warning("⚠️ No matches found.")
    else:
        st.info("🛠️ Set your filters to refine the data.")


        # Price Packages
        price_packages()
        
def price_packages():
    """Display the price packages"""

    st.markdown("""
    <hr style="border:none;height:1px;background-color:#eee;margin:0.5rem 0 0.5rem 0"/>
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="section-title">\U0001F3C6 Pricing Plans</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        .price-card {
            border: 2px dotted #4b8df8 !important;
            border-radius: 12px;
            padding: 25px;
            height: 100%;
            transition: all 0.3s ease;
            position: relative;
            background: white;
        }
        .price-card:hover {
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            transform: translateY(-5px);
        }
        .price-header {
            color: #1e88e5;
            margin-bottom: 5px !important;
            font-size: 24px !important;
        }
        .price-amount {
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }
        .price-period {
            color: #666;
            font-size: 14px;
        }
        .popular-badge {
            position: absolute;
            top: -12px;
            right: -12px;
            background: #add8e6;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            transform: rotate(15deg);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .pricing-button {
            width: 100%;
            margin-top: 15px;
            background: #1e88e5 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    price_cols = st.columns(3)
    with price_cols[0]:
        st.markdown("""
        <div class='price-card'>
            <h3 class='price-header'>Free</h3>
            <div class='price-amount'>$0</div>
            <p><strong>TextDigit Basic</strong></p>
            <ul class='feature-list'>
                <li class='feature-item'>Basic filtering</li>
                <li class='feature-item'>Basic Regex filtering</li>
                <li class='feature-item'>Multiple File Analysis</li>                
                <li class='feature-item'>Custom column filtering</li>                
                <li class='feature-item'>2 column selection</li>                
                <li class='feature-item'>25MB file strorage capacity</li>
                <li class='feature-item'>Email support</li>
            </ul>
        <a href="https://textdigit.com/free-account"> 
            <button class='pricing-button'>Get Free</button>
        </a>
        </div>
        """, unsafe_allow_html=True)

    with price_cols[1]:
        st.markdown("""
        <div class='price-card'>
            <h3 class='price-header'>Professional</h3>
            <div class='price-amount'>$29 per month</div>
            <p><strong>TextDigit Professional</strong></p>
            <ul class='feature-list'>
                <li class='feature-item'>7 day free trial</li>            
                <li class='feature-item'>Basic plan</li>
                <li class='feature-item'>Advanced filtering</li>
                <li class='feature-item'>Advanced Regex filtering</li>
                <li class='feature-item'>5 column selection</li>  
                <li class='feature-item'>1GB file strorage capacity</li>
                <li class='feature-item'>Standard support</li>
                <li class='feature-item'>Cancel anytime</li>  
            </ul>
             <a href="https://khandirect.thrivecart.com/textdigit-professional">           
            <button class='pricing-button'>Get Professional</button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    with price_cols[2]:
        st.markdown("""
        <div class='price-card'>
            <div class='popular-badge'>POPULAR</div>
            <h3 class='price-header'>Premium</h3>
            <div class='price-amount'>$99 per month</div>
            <p><strong>TextDigit Premium+</strong></p>
            <ul class='feature-list'>
                <li class='feature-item'>7 day free trial</li>  
                <li class='feature-item'>Basic plan</li> 
                <li class='feature-item'>Professional plan</li>                 
                <li class='feature-item'>5GB file strorage capacity</li>
                <li class='feature-item'>10 column selection</li>  
                <li class='feature-item'>Priority support</li>
                <li class='feature-item'>Dedicated account manager</li>
                <li class='feature-item'>Cancel anytime</li>  
            </ul>
             <a href="https://khandirect.thrivecart.com/textdigit-premium"> 
            <button class='pricing-button'>Get Premium</button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        .enterprise-box {
            border-left: 4px dotted #1e88e5;
            padding: 20px;
            margin: 30px 0;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .enterprise-title {
            color: #1e88e5;
            margin-bottom: 10px !important;
        }
        .contact-button {
            background: #1e88e5;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            margin-top: 10px;
        }
    </style>

    <div class='enterprise-box'>
        <h4 class='enterprise-title'>TextDigit Enterprise</h4>
        <p>We provide bespoke services for clients with large data dump files to process.</p>
        <p><strong>Includes:</strong></p>
        <ul>
            <li>Custom data processing pipelines</li>
            <li>Complex regex tools</li>
            <li>SQL querying</li>
            <li>Very large data files handling</li>
            <li>Dedicated engineering team</li>
        </ul>
        <a href="https://textdigit.com/enterprise-form"> 
        <button class='contact-button'>Contact Sales</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

