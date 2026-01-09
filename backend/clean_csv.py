import csv
import re
import os


def remove_non_english_characters(text):
    """
    Remove all non-English characters from a string.
    Keeps only ASCII characters (letters, numbers, common punctuation, spaces).
    """
    if not isinstance(text, str):
        return text
    
    # Keep only ASCII printable characters (32-126) and common punctuation
    # This includes: letters (a-z, A-Z), digits (0-9), spaces, and basic punctuation
    cleaned = re.sub(r'[^\x20-\x7E]', '', text)
    
    # Remove extra spaces that might result from removing characters
    cleaned = ' '.join(cleaned.split())
    
    return cleaned


def clean_csv_file(input_file, output_file=None):
    """
    Read a CSV file, remove non-English characters from all fields,
    and save to a new file.
    
    Args:
        input_file: Path to the input CSV file
        output_file: Path to save the cleaned CSV (if None, overwrites input file)
    """
    if output_file is None:
        output_file = input_file
        backup_file = input_file.replace('.csv', '_backup.csv')
        print(f"Creating backup at: {backup_file}")
        os.rename(input_file, backup_file)
        input_file = backup_file
    
    rows_cleaned = 0
    total_rows = 0
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            # Read CSV
            csv_reader = csv.reader(infile)
            rows = list(csv_reader)
            total_rows = len(rows)
            
            # Clean each row
            cleaned_rows = []
            for row in rows:
                cleaned_row = [remove_non_english_characters(field) for field in row]
                cleaned_rows.append(cleaned_row)
                rows_cleaned += 1
        
        # Write cleaned data
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerows(cleaned_rows)
        
        print(f"✓ Successfully cleaned {rows_cleaned} rows")
        print(f"✓ Cleaned file saved to: {output_file}")
        
        if output_file != input_file:
            print(f"✓ Original file preserved at: {input_file}")
        else:
            print(f"✓ Backup saved at: {input_file}")
            
    except Exception as e:
        print(f"✗ Error cleaning CSV: {str(e)}")
        # Restore backup if it exists
        if output_file == input_file and os.path.exists(backup_file):
            os.rename(backup_file, output_file)
            print("✓ Backup restored due to error")
        raise


if __name__ == "__main__":
    # Path to the CSV file
    csv_file_path = "app/pricing.csv"
    
    print(f"Starting to clean CSV file: {csv_file_path}")
    print("-" * 60)
    
    # Clean the CSV file (will create a backup automatically)
    clean_csv_file(csv_file_path)
    
    print("-" * 60)
    print("Done!")
