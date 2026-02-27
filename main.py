import matplotlib.pyplot as plt
import pandas as pd
import os

FILENAME = "my_finances.csv"
expenses = []
incomes = []

print("--- Personal Finance Tracker ---")

#load data
if os.path.exists(FILENAME):
    try:
        existing_df = pd.read_csv(FILENAME)
        for index, row in existing_df.iterrows():
            if row['Type'] == 'Expense':
                expenses.append({'Amount': row['Amount'], 'Date': row['Date'], 'Description': row['Label']})
            else:
                incomes.append({'Amount': row['Amount'], 'Date': row['Date'], 'Resource': row['Label']})
        print(f"File '{FILENAME}' found. Data loaded successfully!")
    except Exception as e:
        print(f"Error loading file: {e}")

#menu
while True:
    action = input("\nMENU\n 1. Add Expense | 2. Add Income | 3. Exit and Plot \nSelection: ")

    match action:
        case '1':
            try:
                description = input("Expense description: ")
                date = input("Date (DD/MM/YYYY): ")
                amount = float(input("Amount: "))
                expenses.append({'Amount': amount, 'Description': description, 'Date': date})
            except ValueError:
                print("Invalid amount. Use numbers like 10.5")
            
        case '2':
            try:
                resource = input("Income resource: ")
                date = input("Date (DD/MM/YYYY): ")
                amount = float(input("Amount: "))
                incomes.append({'Amount': amount, 'Resource': resource, 'Date': date})
            except ValueError:
                print("Invalid amount.")
        case '3':
            print("Generating charts...")
            break
        case _:
            print("Invalid selection.")

#proccess/ plot
if not expenses and not incomes:
    print("No data to display.")
else:
    dfExp = pd.DataFrame(expenses)
    dfInc = pd.DataFrame(incomes)

    if not dfExp.empty: dfExp['Date'] = pd.to_datetime(dfExp['Date'], dayfirst=True)
    if not dfInc.empty: dfInc['Date'] = pd.to_datetime(dfInc['Date'], dayfirst=True)

    # bar chart
    daily_exp = dfExp.groupby('Date')['Amount'].sum() if not dfExp.empty else pd.Series(dtype=float)
    daily_inc = dfInc.groupby('Date')['Amount'].sum() if not dfInc.empty else pd.Series(dtype=float)
    chart_df = pd.concat([daily_inc, daily_exp], axis=1).fillna(0)
    chart_df.columns = ['Income', 'Expenses']
    
    chart_df.plot(kind='barh', figsize=(10, 5), color=['blue', 'orange'])
    plt.title("Daily Overview")
    plt.tight_layout()
    plt.show()

    #pie chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    if not dfExp.empty:
        exp_data = dfExp.groupby('Description')['Amount'].sum()
        ax1.pie(exp_data, labels=exp_data.index, autopct='%1.1f%%')
        ax1.set_title("Expenses")
    
    if not dfInc.empty:
        inc_data = dfInc.groupby('Resource')['Amount'].sum()
        ax2.pie(inc_data, labels=inc_data.index, autopct='%1.1f%%')
        ax2.set_title("Income")
    plt.show()

    # save data to csv
    save_data = []
    for e in expenses:
        save_data.append({'Amount': e['Amount'], 'Date': e['Date'], 'Label': e['Description'], 'Type': 'Expense'})
    for i in incomes:
        save_data.append({'Amount': i['Amount'], 'Date': i['Date'], 'Label': i['Resource'], 'Type': 'Income'})
    
    pd.DataFrame(save_data).to_csv(FILENAME, index=False)
    print(f"All data saved to {FILENAME}")
