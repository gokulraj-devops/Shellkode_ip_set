import pandas as pd
import re

def clean_ipv4(ip):
    if pd.isna(ip):
        return None

    ip = str(ip).replace('[.]', '.').replace(' ', '').strip()
    if ':' in ip:
        return None

    ipv4_pattern = r'^(?:\d{1,3}\.){3}\d{1,3}$'
    if re.match(ipv4_pattern, ip):
        octets = ip.split('.')
        if all(0 <= int(o) <= 255 for o in octets):
            return f"{ip}/32"
    return None

def process_excel(input_file, output_file, ip_column_name='IP'):
    # Load Excel
    df = pd.read_excel(input_file)

    # Clean IPs
    df['Cleaned_IP'] = df[ip_column_name].apply(clean_ipv4)
    df_cleaned = df.dropna(subset=['Cleaned_IP'])

    # Get list of cleaned IPs
    cleaned_ips = df_cleaned['Cleaned_IP'].tolist()

    # Split into two lists
    first_batch = cleaned_ips[:9999]
    second_batch = cleaned_ips[9999:]

    # Pad shorter list with empty strings so both columns align
    max_len = max(len(first_batch), len(second_batch))
    first_batch += [''] * (max_len - len(first_batch))
    second_batch += [''] * (max_len - len(second_batch))

    # Create new DataFrame with two columns
    output_df = pd.DataFrame({
        'Cleaned_IP_SET_1': first_batch,
        'Cleaned_IP_SET_2': second_batch
    })

    # Write to Excel
    output_df.to_excel(output_file, index=False)
    print(f"✅ Processed IPs saved to: {output_file}")

# Example usage
if __name__ == "__main__":
    input_excel = r"raw_ips.xlsx"
    output_excel = r"cleaned_ips.xlsx"
    ip_column = "IP"  # Your column name in Excel
    process_excel(input_excel, output_excel, ip_column)
