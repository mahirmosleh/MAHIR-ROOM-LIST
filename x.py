import json

def convert_accounts(input_file, output_file):
    """Convert account list format to dict format"""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            accounts_list = json.load(f)

        accounts_dict = {}
        for account in accounts_list:
            uid = str(account.get("uid"))
            password = account.get("password")
            if uid and password:
                accounts_dict[uid] = password

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(accounts_dict, f, indent=2, ensure_ascii=False)

        print(f"✅ Converted JSON saved to '{output_file}'")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    input_file = "accounts_list.json"
    output_file = "accs.json"
    convert_accounts(input_file, output_file)
