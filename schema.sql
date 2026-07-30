-- Limpiar tablas si ya existen para poder reiniciar la BD si es necesario
DROP TABLE IF EXISTS sale_items;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS users;

-- 1. Tabla de Usuarios
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'cajero')) NOT NULL DEFAULT 'cajero',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Categorías
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- 3. Tabla de Proveedores
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_person TEXT,
    phone TEXT,
    email TEXT
);

-- 4. Tabla de Clientes
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    document_id TEXT UNIQUE,
    phone TEXT,
    email TEXT
);

-- 5. Tabla de Productos (Relacionada con Categorías y Proveedores)
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    barcode TEXT UNIQUE,
    cost_price REAL NOT NULL,
    sale_price REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    min_stock INTEGER NOT NULL DEFAULT 3,
    category_id INTEGER,
    supplier_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories (id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
);

-- 6. Tabla de Ventas (Encabezado - Relacionada con Usuarios y Clientes)
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL,
    payment_method TEXT CHECK(payment_method IN ('efectivo', 'transferencia', 'tarjeta')) NOT NULL,
    user_id INTEGER NOT NULL,
    customer_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

-- 7. Tabla Detalle de Venta (Tabla Pivot - Relacionada con Ventas y Productos)
CREATE TABLE sale_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales (id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (id)
);