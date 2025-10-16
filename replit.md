# Overview

This is a **Flask-based REST API** for Iranian stock market analysis and prediction. The application provides comprehensive technical analysis, fundamental data tracking, machine learning predictions, and automated trading signal generation for stocks listed on the Tehran Stock Exchange (TSE) and Iran Fara Bourse (IFB).

**Core Purpose:**
- Fetch and process historical and real-time stock data from Iranian market APIs (BRSAPI, TSETMC)
- Perform technical analysis using 20+ indicators (RSI, MACD, Bollinger Bands, custom indicators)
- Generate trading signals through multiple strategies (Golden Key, Weekly Watchlist, Potential Buy Queues)
- Provide ML-based price predictions using Random Forest models
- Track and evaluate signal performance over time
- Deliver market overview data including indices, commodities, and sector analysis

**Key Features:**
- JWT-based authentication
- Swagger/OpenAPI documentation via Flask-RESTX
- Scheduled tasks for automated data updates and analysis
- Persian (Jalali) calendar integration
- SQLAlchemy ORM with Flask-Migrate for database management

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Technology Stack

**Backend Framework:**
- Flask with Flask-RESTX for RESTful API and auto-documentation
- Python 3.x with extensive data science libraries (pandas, numpy, scikit-learn, ta)

**Database:**
- SQLAlchemy ORM with support for SQLite (development) and PostgreSQL (production)
- Flask-Migrate (Alembic) for database migrations
- Connection pooling and thread-safe configuration for concurrent access

**Authentication & Security:**
- Flask-JWT-Extended for stateless JWT token authentication
- Flask-Bcrypt for password hashing
- CORS enabled via Flask-CORS for cross-origin requests
- Separate SECRET_KEY and JWT_SECRET_KEY for Flask sessions and JWT signing

**Task Scheduling:**
- Flask-APScheduler for periodic background jobs (data fetching, analysis, ML predictions)
- Runs daily/weekly/monthly tasks for market analysis and signal evaluation

**Persian Calendar:**
- jdatetime library for Jalali (Persian) date handling
- All dates stored in both Gregorian and Jalali formats

## Data Models & Database Schema

**Core Entities:**

1. **User** - Authentication and user management
   - Basic fields: username, email, hashed_password
   - Used for JWT token generation

2. **ComprehensiveSymbolData** - Master symbol/stock registry
   - Symbol identifiers: symbol_id (PK), symbol_name, tse_index, ISIN
   - Fundamental data: EPS, P/E ratio, P/S ratio, NAV, market cap, float shares
   - Classification: market_type, group_name, industry, sector
   - Update tracking: last_historical_update_date, last_fundamental_update_date

3. **HistoricalData** - Time-series price and volume data
   - OHLCV data with additional Iranian market fields (final price, yesterday price)
   - Volume breakdown: buy/sell volumes for institutional and individual traders
   - Technical context: count of trades, value of trades
   - Jalali date indexing for Persian calendar queries

4. **TechnicalIndicatorData** - Calculated technical indicators
   - Trend: SMA, EMA, MACD (line, signal, histogram)
   - Momentum: RSI, Stochastic (K, D)
   - Volatility: Bollinger Bands (upper, middle, lower), ATR
   - Volume: Volume MA, Smart Money Flow
   - Custom: Squeeze Momentum, Halftrend Signal, Resistance levels

5. **FundamentalData** - Fundamental metrics snapshot
   - Valuation: P/E, P/B ratios
   - Profitability: EPS, ROE, profit margin
   - Balance sheet: debt ratio, current ratio
   - Update timestamp tracking

6. **CandlestickPatternDetection** - Pattern recognition results
   - Detected patterns with boolean flags (Bullish Engulfing, Hammer, Doji, etc.)
   - Pattern strength/confidence scores

7. **MLPrediction** - Machine learning prediction results
   - Model-generated predictions: predicted_trend, confidence_score
   - Feature importance tracking
   - Actual outcome tracking for model evaluation

**Signal Generation Models:**

8. **GoldenKeyResult** - High-quality stock filtering
   - Symbols passing multiple technical filter criteria
   - Scoring system based on matched filters
   - Entry/exit tracking with profit/loss calculation
   - Status: active, closed_profit, closed_loss, closed_neutral

9. **WeeklyWatchlistResult** - Weekly curated stock picks
   - Selected symbols with entry recommendations
   - Outlook and reasoning for selection
   - Performance tracking with exit prices and P/L percentages

10. **PotentialBuyQueueResult** - Buy queue detection
    - Symbols showing accumulation patterns
    - Power thrust signals and smart money flow indicators
    - General vs. fund-specific queues

**Performance Tracking:**

11. **SignalsPerformance** - Individual signal outcomes
    - Links to signal source (Golden Key, Weekly Watchlist)
    - Entry/exit prices and dates
    - Win/loss/neutral classification
    - Profit/loss percentage calculation

12. **AggregatedPerformance** - Performance metrics by period
    - Aggregation levels: daily, weekly, monthly, annual
    - Win rate, average profit/loss, net profit metrics
    - Breakdown by signal source

13. **DailySectorPerformance** - Sector-level analysis
    - Daily sector rankings by trade value and money flow
    - Industry group performance tracking

## External Dependencies

**Data Sources:**

1. **BRSAPI (brsapi.ir)** - Primary data provider
   - Historical EOD (End-of-Day) data for all symbols
   - Symbol metadata and fundamental information
   - Market indices (Total Index, Equal-Weighted, etc.)
   - API Key authentication required
   - Used in: `fetch_latest_brsapi_eod.py`, `iran_market_data.py`

2. **TSETMC (tsetmc.com)** - Tehran Stock Exchange official site
   - Real-time and historical data scraping
   - Fallback when BRSAPI unavailable
   - Used via pytse_client wrapper in: `pytse_wrapper.py`

3. **TGJU (tgju.org)** - Gold and currency prices
   - Web scraping for Iranian gold prices (18k, coin, etc.)
   - Caching mechanism to reduce request frequency
   - Proxy service in: `tgju.py`

4. **Metals.dev API** - Global commodity prices
   - Real-time prices for gold, silver, platinum, copper
   - USD-based pricing with API key authentication
   - Configuration: `METALS_DEV_API_KEY` in Flask config

**Third-Party Libraries:**

1. **pytse_client** - Python wrapper for TSE data
   - Symbol search and historical data fetching
   - Enhanced with custom retry logic and error handling in `pytse_wrapper.py`

2. **ta (Technical Analysis Library)** - Technical indicator calculation
   - RSI, MACD, Bollinger Bands, Stochastic, ATR, etc.
   - Used extensively in technical analysis services

3. **scikit-learn** - Machine learning framework
   - Random Forest classifier for trend prediction
   - Model serialization with joblib
   - Training: `train_model.py`, Inference: `ml_predictor.py`

**Service Architecture:**

- **Data Fetching Services:**
  - `data_fetch_and_process.py` - Main data orchestration
  - `fetch_latest_brsapi_eod.py` - BRSAPI data fetching
  - `fetch_full_historical_pytse.py` - Full history backfill
  - `symbol_initializer.py` - Initial symbol population

- **Analysis Services:**
  - `analysis_service.py` - Core technical analysis logic
  - `golden_key_service.py` - Multi-filter stock screening
  - `weekly_watchlist_service.py` - Weekly stock selection
  - `potential_buy_queues_service.py` - Buy queue detection
  - `sector_analysis_service.py` - Industry sector analysis
  - `market_analysis_service.py` - Market overview and sentiment

- **ML Services:**
  - `ml_prediction_service.py` - Prediction generation and evaluation
  - `train_model.py` - Model training pipeline
  - `ml_predictor.py` - Model loading and inference

- **Performance Services:**
  - `performance_service.py` - Signal evaluation and aggregation

- **Utility Services:**
  - `historical_data_service.py` - Historical data queries
  - `utils.py` - Shared utility functions (date conversion, indicators)

**Scheduled Tasks (scheduler.py):**

- Daily: Data updates, technical analysis, candlestick detection, sector analysis
- Weekly: Watchlist selection, ML predictions, performance evaluation
- On-demand: Full historical backfill, manual analysis triggers

**API Routes (Flask Blueprints):**

- `/api/auth` - User registration and login
- `/api/analysis` - Technical analysis endpoints
- `/api/golden_key` - Golden Key signals
- `/api/weekly_watchlist` - Weekly picks
- `/api/potential_queues` - Buy queue signals
- `/api/performance` - Performance metrics
- `/api/market-overview` - Market data aggregation

**Configuration Management:**

- Environment variables for sensitive data (API keys, secrets)
- Separate development (SQLite) and production (PostgreSQL) database URIs
- Flask-Migrate for version-controlled schema changes
- Database connection pooling with pre-ping health checks

**Deployment Considerations:**

- Designed for Replit deployment with Docker compatibility
- Graceful handling of DATABASE_URL from hosting environment
- SQLite fallback for local development
- Thread-safe database sessions with proper context management
- Scheduled tasks run in separate threads via APScheduler
- CORS configured for frontend integration