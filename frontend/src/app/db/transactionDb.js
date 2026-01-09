import Database from 'better-sqlite3';

const transactionDb = new Database('transactions.db', { verbose: console.log });

console.log('Transaction DB initialized at:', 'transactions.db');

transactionDb.exec(`
  CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER,
    amount INTEGER,
    type TEXT,
    date TEXT,
    remarks TEXT
   
  )
`);

console.log('Transaction table created/verified');

export default transactionDb;
