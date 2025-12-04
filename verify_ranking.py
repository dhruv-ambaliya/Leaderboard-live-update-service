import pandas as pd

def clean_value(val):
    if pd.isna(val) or val == '-' or val == 'D$Q':
        return 0
    return float(val)

def get_countback_key(row, round_cols):
    scores = []
    for col in round_cols:
        scores.append(clean_value(row[col]))
    scores.sort(reverse=True)
    return scores

def verify_ranking():
    input_file = 'leaderboard_sorted.xlsx'
    
    # Load the sorted file
    # We need to find the header again
    df_all = pd.read_excel(input_file, sheet_name='Leaderboard', header=None)
    
    top_header_idx = -1
    for idx, row in df_all.iterrows():
        if 'Pos' in str(row.values) and 'Player' in str(row.values):
            top_header_idx = idx
            break
            
    if top_header_idx == -1:
        print("Could not find Leaderboard table.")
        return

    df_top = df_all.iloc[top_header_idx:].copy()
    
    # Rename columns logic (same as rank script)
    new_columns = ['Pos', 'Player']
    for i in range(1, 25):
        new_columns.append(f'R{i:02d}')
    new_columns.extend(['Points', 'Spent ($m)', '$m/Pt'])
    
    # Fallback if length mismatch
    if len(new_columns) != df_top.shape[1]:
        cols = list(df_top.iloc[0])
        counts = {}
        new_columns = []
        for c in cols:
            if c not in counts:
                counts[c] = 0
                new_columns.append(c)
            else:
                counts[c] += 1
                new_columns.append(f"{c}.{counts[c]}")
                
    df_top.columns = new_columns
    df_top = df_top.iloc[1:]
    
    last_player_idx_top = -1
    for i in range(len(df_top)):
        val = df_top.iloc[i]['Player']
        if str(val) == 'Points Totals' or pd.isna(val):
            last_player_idx_top = i
            break
            
    if last_player_idx_top != -1:
        df_players = df_top.iloc[:last_player_idx_top].copy()
    else:
        df_players = df_top.copy()
        
    # Round columns
    round_cols = [c for c in df_players.columns if str(c).startswith('R') and len(str(c)) == 3 and c[1:].isdigit()]
    
    # Verify Order
    print("Verifying order...")
    previous_row = None
    
    for idx, row in df_players.iterrows():
        if previous_row is None:
            previous_row = row
            continue
            
        # Check Points (Desc)
        curr_pts = clean_value(row.get('Points', 0) if 'Points' in row else row.get('Total Points', 0))
        prev_pts = clean_value(previous_row.get('Points', 0) if 'Points' in previous_row else previous_row.get('Total Points', 0))
        
        if curr_pts > prev_pts:
            print(f"FAIL: Points not descending at row {idx}. Prev: {prev_pts}, Curr: {curr_pts}")
            
        elif curr_pts == prev_pts:
            # Check Spending (Asc)
            curr_spend = clean_value(row.get('Spent ($m)', 0))
            prev_spend = clean_value(previous_row.get('Spent ($m)', 0))
            
            if curr_spend < prev_spend:
                print(f"FAIL: Spending not ascending for tied points at row {idx}. Prev: {prev_spend}, Curr: {curr_spend}")
                
            elif curr_spend == prev_spend:
                # Check Countback (Desc)
                curr_cb = get_countback_key(row, round_cols)
                prev_cb = get_countback_key(previous_row, round_cols)
                
                if curr_cb > prev_cb:
                     print(f"FAIL: Countback not descending for tied points/spend at row {idx}. Prev: {prev_cb}, Curr: {curr_cb}")
                
                elif curr_cb == prev_cb:
                    # Check Name (Asc)
                    curr_name = str(row['Player'])
                    prev_name = str(previous_row['Player'])
                    
                    if curr_name < prev_name:
                        print(f"FAIL: Name not ascending for tied everything at row {idx}. Prev: {prev_name}, Curr: {curr_name}")
                    else:
                        print(f"TIED: {prev_name} and {curr_name} are tied.")
        
        previous_row = row
        
    print("Verification complete.")

if __name__ == "__main__":
    verify_ranking()
