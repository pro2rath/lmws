-- This schema is for MySQL

CREATE TABLE workers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(15) NOT NULL UNIQUE,
    work_type VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    aadhaar_path VARCHAR(255),
    rationcard_path VARCHAR(255),
    selfie_path VARCHAR(255) NOT NULL,
    verified_status INT NOT NULL DEFAULT 0,
    is_blocked INT NOT NULL DEFAULT 0,
    last_available_date DATE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE complaints (
    id INT PRIMARY KEY AUTO_INCREMENT,
    worker_id INT NOT NULL,
    reason TEXT NOT NULL,
    submitted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (worker_id) REFERENCES workers(id) ON DELETE CASCADE
);

CREATE TABLE work_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    worker_id INT NOT NULL,
    work_date DATE NOT NULL,
    before_work_image_path VARCHAR(255) NOT NULL,
    after_work_image_path VARCHAR(255) NOT NULL,
    rating INT,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (worker_id) REFERENCES workers(id) ON DELETE CASCADE
);