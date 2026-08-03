# 📈 Yahoo Finance Stock Data Collection and Paper Trading Platform

## Overview

This project is a complete end-to-end stock market platform designed to collect, process, store, and visualize financial market data.

It was developed from the ground up as a modular system that combines data engineering, backend development, automation, database optimization, and a modern web interface.

The platform includes:

- Automated stock data collection from Yahoo Finance
- JSON-based data storage
- Automatic JSON-to-SQL conversion
- Duplicate detection and prevention during imports
- Automatic database index creation for optimized performance
- Daily automated updates using a Systemd service
- A modern web application
- A paper trading (virtual trading) platform
- Interactive charts and market analytics
- Financial news integration
- A personal assistant for portfolio management and market exploration

---

# Project Goals

The primary goal of this project is to provide a fully automated system capable of:

- Collecting up-to-date stock market data
- Storing large datasets efficiently
- Providing fast database queries
- Supporting historical market analysis
- Presenting financial information through a clean and intuitive web interface

The project demonstrates the complete workflow, from data acquisition to visualization.

---

# Data Collection

The platform automatically retrieves stock information from Yahoo Finance.

Collected information includes:

- Current price
- Open price
- Previous close
- Daily high
- Daily low
- Trading volume
- Market capitalization
- Price-to-Earnings ratio
- Dividend information
- Company sector
- Industry classification
- Company profile
- Additional financial statistics

Each company's data is stored as a JSON document, allowing easy backups, processing, and future imports.

---

# Automated Daily Updates

The project includes a Systemd service responsible for automating data collection.

The service:

- Starts automatically with the operating system
- Executes the data collection scripts every day
- Refreshes all market information
- Requires no manual intervention

This ensures that the local database remains synchronized with the latest available market data.

---

# JSON to SQL Conversion

The project contains a dedicated importer that converts the collected JSON files into an SQL database.

Features include:

- Automatic parsing of thousands of JSON files
- Automatic table creation
- Automatic index generation
- Duplicate detection
- Duplicate prevention
- Safe repeated imports without creating duplicate records

Because of this approach, the importer can be executed multiple times while maintaining database integrity.

---

# Web Application

The platform includes a complete web application built with Python, Flask, Docker, and Nginx.

Main features include:

- Stock search
- Individual company pages
- Financial statistics
- Interactive charts
- Market news
- Fast navigation
- Responsive interface
- Database integration

Deployment is handled using Docker Compose with separate services for:

- Flask application
- Nginx web server

This architecture makes deployment, maintenance, and scaling straightforward.

---

# Paper Trading Platform

The project includes a fully functional paper trading system that simulates real-world investing.

Users can:

- Buy stocks
- Sell stocks
- Build a virtual investment portfolio
- Track profits and losses
- Monitor portfolio value
- Analyze trading performance over time

This allows users to experiment with investment strategies without risking real money.

---

# Personal Assistant

The platform includes a personal assistant designed to simplify navigation and market analysis.

The assistant helps users:

- Access stock information quickly
- Explore financial data
- Navigate platform features
- Retrieve relevant market information efficiently

---

# Financial News

The application integrates financial news to provide additional market context.

This allows users to better understand events that may influence stock prices and market behavior.

---

# Performance

The platform was designed with performance and scalability in mind.

Special attention was given to:

- Fast database queries
- Automatic indexing
- Duplicate prevention
- Efficient memory usage
- Reliable automated updates

These optimizations allow the platform to handle large datasets efficiently.

---

# Project Structure

The project is organized into multiple independent components:

- Data collection engine
- JSON data repository
- JSON-to-SQL conversion system
- SQL database
- Flask web application
- Nginx reverse proxy
- Docker Compose configuration
- Systemd automation services
- Public web assets
- News module
- Paper trading engine
- Charts and analytics
- Personal assistant

This modular design makes the project easier to maintain and extend.

---

# Technologies Used

The project is built using the following technologies:

- Python
- Flask
- SQLite / SQL
- JSON
- Docker
- Docker Compose
- Nginx
- Linux
- Systemd
- HTML
- CSS
- JavaScript

---

# Purpose

This project was created as a practical demonstration of building a complete financial data platform.

It combines multiple areas of software engineering, including:

- Data collection
- Data engineering
- Database design
- Backend development
- Web development
- Infrastructure automation
- Containerization

The system demonstrates how to build a complete pipeline that starts with collecting financial data, processes and stores it efficiently, and finally presents it through a modern, responsive web interface.

---

# Future Improvements

Potential future enhancements include:

- User authentication and account management
- Watchlists
- Real-time market data support
- Additional financial indicators
- REST API
- Portfolio performance analytics
- Email notifications
- Mobile-friendly interface improvements
- AI-assisted market analysis
- Support for multiple database engines

---

# License

This project is intended for educational and research purposes.

Please review Yahoo Finance's terms of service before using this software to collect or redistribute financial data.
