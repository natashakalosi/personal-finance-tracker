import matplotlib.pyplot as plt
import pandas as pd
import os

FILENAME = "my_finances.csv"

def load_data():
    #Loads financial data from the CSV file and returns lists of entries
    expenses, incomes = [], []
    if os.path.exists(FILENAME):
        try:
            df = pd.read_csv(FILENAME)
            # Standardize dates during loading
            df['Date'] = pd.to_datetime(df['Date'])
            
            for _, row in df.iterrows():
                item = {'Amount': row['Amount'], 'Date': row['Date'], 'Label': row['Label']}
                if row['Type'] == 'Expense':
                    expenses.append(item)
                else:
                    incomes.append(item)
            print(f"Data successfully loaded from {FILENAME}")
        except Exception as e:
            print(f" Error loading file: {e}")
    return expenses, incomes

def get_user_input(entry_type):
    #Prompts user for transaction details and returns a dictionary
    try:
        label = input(f"{entry_type} description/source: ")
        date_str = input("Date (DD/MM/YYYY): ")
        # Validate date format immediately
        date = pd.to_datetime(date_str, dayfirst=True)
        amount = float(input("Amount: "))
        return {'Amount': amount, 'Label': label, 'Date': date}
    except ValueError:
        print("Invalid input. Transaction cancelled. Please use numbers for amounts.")
        return None

def plot_results(expenses, incomes):
    #Generates visualization charts using Matplotlib."""
    if not expenses and not incomes:
        print("No data available to plot.")
        return

    df_exp = pd.DataFrame(expenses)
    df_inc = pd.DataFrame(incomes)

    # 1. Bar Chart: Daily Totals
    plt.figure(figsize=(10, 5))
    daily_exp = df_exp.groupby('Date')['Amount'].sum() if not df_exp.empty else pd.Series(dtype=float)
    daily_inc = df_inc.groupby('Date')['Amount'].sum() if not df_inc.empty else pd.Series(dtype=float)
    
    chart_df = pd.concat([daily_inc, daily_exp], axis=1).fillna(0)
    chart_df.columns = ['Income', 'Expenses']
    chart_df.plot(kind='barh', color=['#2ecc71', '#e74c3c'], figsize=(10, 5))
    plt.title("Daily Financial Overview")
    plt.xlabel("Amount")
    plt.tight_layout()
    plt.show()

    # 2. Pie Charts: Distribution by Category/Label
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    if not df_exp.empty:
        exp_dist = df_exp.groupby('Label')['Amount'].sum()
        ax1.pie(exp_dist, labels=exp_dist.index, autopct='%1.1f%%', startangle=140)
        ax1.set_title("Expense Distribution")
    
    if not df_inc.empty:
        inc_dist = df_inc.groupby('Label')['Amount'].sum()
        ax2.pie(inc_dist, labels=inc_dist.index, autopct='%1.1f%%', startangle=140)
        ax2.set_title("Income Sources")
    
    plt.tight_layout()
    plt.show()

def save_data(expenses, incomes):
    #Consolidates data and saves it back to the CSV file
    combined_data = []
    for e in expenses:
        combined_data.append({**e, 'Type': 'Expense'})
    for i in incomes:
        combined_data.append({**i, 'Type': 'Income'})
    
    if combined_data:
        pd.DataFrame(combined_data).to_csv(FILENAME, index=False)
        print(f"Data saved to {FILENAME}")

def main():
    #Main program loop
    print("--- PERSONAL FINANCE TRACKER ---")
    expenses, incomes = load_data()

    while True:
        print("\n[ MENU ]")
        print("1. Add Expense")
        print("2. Add Income")
        print("3. Save, Plot & Exit")
        
        choice = input("Select an option: ")

        if choice == '1':
            entry = get_user_input("Expense")
            if entry: expenses.append(entry)
        elif choice == '2':
            entry = get_user_input("Income")
            if entry: incomes.append(entry)
        elif choice == '3':
            save_data(expenses, incomes)
            plot_results(expenses, incomes)
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()

