# 🚗 Ola Rides Power BI Dashboard - Complete Setup Guide

## Overview
This guide provides step-by-step instructions to create an interactive Power BI dashboard for analyzing Ola ride-sharing data with visualizations for ride trends, revenue, cancellations, and key business metrics.

---

## 📋 Prerequisites

- **Power BI Desktop** (latest version)
- **Access to data source**:
  - PostgreSQL database with `july_rides` table, OR
  - CSV file from `data/july_rides.csv`
- **Basic Power BI knowledge** (data modeling, DAX, visualizations)

---

## 🔌 Step 1: Connect Data Source

### Option A: Connect to PostgreSQL Database

1. Open Power BI Desktop
2. Click **Get Data** → **More**
3. Search for **PostgreSQL database**
4. Enter connection details:
   - **Server**: localhost
   - **Database**: ola_ride_insights
   - **Data Connectivity mode**: Import
5. Click **OK**
6. Enter credentials:
   - **Username**: postgres
   - **Password**: [your password]
7. Select the `july_rides` table and click **Load**

### Option B: Connect to CSV File

1. Click **Get Data** → **Text/CSV**
2. Navigate to `data/july_rides.csv`
3. Click **Load**
4. In Power Query Editor, ensure data types are correct
5. Click **Close & Apply**

---

## 📊 Step 2: Data Transformation & Modeling

### Transform Data in Power Query

1. **Date Column**: Right-click `Date` column → **Change Type** → **Date/Time**
2. **Numeric Columns**: Convert to appropriate types:
   - `Booking_Value` → Decimal Number
   - `Ride_Distance` → Decimal Number
   - `Driver_Ratings` → Decimal Number
   - `Customer_Rating` → Decimal Number

3. **Add Helper Columns**:
   ```
   Hour = HOUR([Date])
   Day_of_Week = WEEKDAY([Date], 2)
   Week_Number = WEEKNUM([Date])
   Month = MONTH([Date])
   Date_Only = INT([Date])
   ```

4. Click **Close & Apply**

### Create Data Model

1. Go to **Model** view
2. Create relationships:
   - Set `Booking_ID` as unique identifier (Primary Key)
   
3. Create calculated columns (see DAX Formulas section)

---

## 📐 Step 3: Create DAX Formulas & Measures

See `DAX_FORMULAS.md` for complete formulas. Key measures to create:

### KPI Measures
```
Total Rides = COUNTA('july_rides'[Booking_ID])
Total Revenue = SUM('july_rides'[Booking_Value])
Successful Rides = CALCULATE(COUNTA('july_rides'[Booking_ID]), 'july_rides'[Booking_Status]="Success")
Canceled Rides = CALCULATE(COUNTA('july_rides'[Booking_ID]), 'july_rides'[Booking_Status]<>"Success")
Cancellation Rate = DIVIDE([Canceled Rides], [Total Rides], 0) * 100
```

### Advanced Measures
```
Avg Revenue per Ride = DIVIDE([Total Revenue], [Total Rides], 0)
Avg Driver Rating = AVERAGE('july_rides'[Driver_Ratings])
Avg Customer Rating = AVERAGE('july_rides'[Customer_Rating])
Revenue per KM = DIVIDE([Total Revenue], SUM('july_rides'[Ride_Distance]), 0)
```

---

## 🎨 Step 4: Create Interactive Visualizations

### Page 1: Executive Summary

| Visualization | Type | Fields |
|---|---|---|
| Total Rides | Card | [Total Rides] |
| Total Revenue | Card | [Total Revenue] |
| Success Rate | Card | [Success Rate %] |
| Cancellation Rate | Card | [Cancellation Rate] |
| Avg Driver Rating | Card | [Avg Driver Rating] |
| Avg Customer Rating | Card | [Avg Customer Rating] |

### Page 2: Ride Trends & Performance

1. **Daily Ride Volume**
   - Type: Line Chart
   - X-axis: Date
   - Y-axis: Count of Booking_ID
   - Legend: Booking_Status

2. **Hourly Distribution Heatmap**
   - Type: Matrix
   - Rows: Day of Month
   - Columns: Hour of Day
   - Values: Count of Booking_ID

3. **Peak Hours Analysis**
   - Type: Combo Chart (Column + Line)
   - X-axis: Hour
   - Column Y-axis: Total Rides
   - Line Y-axis: Total Revenue

4. **Booking Status Breakdown**
   - Type: Pie Chart
   - Legend: Booking_Status
   - Values: Count of Booking_ID

### Page 3: Revenue Analysis

1. **Daily Revenue Trend**
   - Type: Area Chart
   - X-axis: Date
   - Y-axis: Sum of Booking_Value

2. **Revenue by Vehicle Type**
   - Type: Bar Chart
   - Axis: Vehicle_Type
   - Value: Sum of Booking_Value

3. **Revenue by Payment Method**
   - Type: Donut Chart
   - Legend: Payment_Method
   - Values: Sum of Booking_Value

4. **Revenue Distribution**
   - Type: Histogram
   - Field: Booking_Value
   - Bins: 20-30

### Page 4: Cancellation Analysis

1. **Cancellation Status Breakdown**
   - Type: Stacked Bar Chart
   - Axis: Booking_Status
   - Value: Count of Booking_ID

2. **Cancellation Rate by Vehicle Type**
   - Type: Bar Chart with Conditional Formatting
   - Axis: Vehicle_Type
   - Value: [Cancellation Rate]

3. **Top Cancellation Reasons**
   - Type: Horizontal Bar Chart
   - Axis: Incomplete_Rides_Reason
   - Value: Count of Booking_ID

4. **Cancellation Trend Over Time**
   - Type: Line Chart
   - X-axis: Date
   - Y-axis: Count of Canceled Bookings
   - Legend: Cancel Reason Categories

### Page 5: Location & Vehicle Performance

1. **Top 10 Pickup Locations**
   - Type: Bar Chart
   - Axis: Pickup_Location (Top 10)
   - Value: Count of Booking_ID

2. **Top 10 Drop Locations**
   - Type: Bar Chart
   - Axis: Drop_Location (Top 10)
   - Value: Count of Booking_ID

3. **Vehicle Type Performance Matrix**
   - Type: Table
   - Columns: Vehicle_Type, Total Rides, Revenue, Avg Rating

4. **Vehicle Distribution**
   - Type: Pie Chart
   - Legend: Vehicle_Type
   - Values: Count of Booking_ID

---

## 🔍 Step 5: Add Interactive Filters & Slicers

### Slicers to Add (on each page or dedicated filter page)

1. **Date Range Slicer**
   - Field: Date
   - Style: Between/Range
   - Format: Date

2. **Vehicle Type Slicer**
   - Field: Vehicle_Type
   - Style: Button (Multiple Select)

3. **Booking Status Slicer**
   - Field: Booking_Status
   - Style: Dropdown

4. **Payment Method Slicer**
   - Field: Payment_Method
   - Style: Button

5. **Revenue Range Slicer**
   - Field: Booking_Value
   - Style: Numeric Range

6. **Driver Rating Slicer**
   - Field: Driver_Ratings
   - Style: Numeric Range

### Configure Slicer Interactions

1. Select a slicer
2. Click **Edit Interactions** (Visual Tools ribbon)
3. For each visual, click the interaction button:
   - Filter (✓) - Apply slicer
   - Highlight (◐) - Highlight matching data
   - None (⊘) - Ignore slicer

---

## 🎯 Step 6: Create KPI Indicators

For key metrics, add KPI visuals:

1. **Trend KPIs**
   - **Total Revenue KPI**
     - Value: [Total Revenue]
     - Trend Axis: Date
     - Target: Set target based on goals
   
   - **Success Rate KPI**
     - Value: [Success Rate %]
     - Target: 95%
   
   - **Driver Rating KPI**
     - Value: [Avg Driver Rating]
     - Target: 4.5
     - Statuses: Green (>4.5), Yellow (4-4.5), Red (<4)

2. **Gauge Charts for Percentages**
   - Cancellation Rate (Target: <10%)
   - Success Rate (Target: >90%)

---

## 🎬 Step 7: Dashboard Layout

### Recommended Dashboard Structure

**Page 1: Executive Overview**
- Top 6 KPI cards
- 2x2 grid of key metrics
- Single interactive filter pane

**Page 2: Ride Trends**
- Daily volume line chart (full width)
- Hourly heatmap + Peak hours combo chart
- Status distribution pie chart
- Booking Status slicer

**Page 3: Revenue Insights**
- Daily revenue area chart (full width)
- 2x2 grid: Vehicle Type, Payment Method, Distribution, Trend
- Revenue range slicer

**Page 4: Cancellations Deep Dive**
- Status breakdown chart
- Reasons analysis (top 10)
- Trend over time line chart
- Vehicle Type cancellation rates

**Page 5: Location & Vehicle Analysis**
- Top pickup/drop locations (2 charts)
- Vehicle performance table
- Vehicle distribution pie
- Location filter options

---

## 📱 Step 8: Mobile Optimization

Power BI mobile dashboards require optimization:

1. In Power BI Service, click **Edit** on dashboard
2. Click **Mobile Layout** (phone icon)
3. Arrange visuals for vertical scrolling (1 column)
4. Hide less critical visuals for mobile
5. Test on phone preview

---

## 🚀 Step 9: Publishing & Sharing

### Publish to Power BI Service

1. In Power BI Desktop, click **Publish**
2. Select workspace (or create new)
3. Wait for publishing to complete

### Share Dashboard

1. Go to Power BI Service
2. Click dashboard
3. Click **Share** (top right)
4. Enter email addresses
5. Set permissions:
   - **View** - Can view only
   - **Edit** - Can view and edit
   - **Reshare** - Can share with others

### Set Up Refresh Schedule

1. In Power BI Service, go to **Dataset**
2. Click **Settings** (⋯)
3. Configure **Scheduled refresh**:
   - Frequency: Daily
   - Time: Off-peak hours
   - Frequency: Multiple times per day (if needed)

---

## 📊 Step 10: Advanced Features

### Drill-Through Pages

Create summary and detail pages with drill-through:

1. **Summary Page**: Vehicle Type metrics
2. **Detail Page**: Individual vehicle performance
3. Add drill-through filter from summary to detail

### Bookmarks & Navigation

1. Create bookmarks for different views
2. Add **Buttons** with bookmark actions
3. Create navigation menu:
   - "Show All"
   - "Filter by Date"
   - "Compare YoY"

### Q&A Feature

Enable natural language queries:

1. Go to dataset settings
2. Enable **Q&A**
3. Define synonyms for key terms
4. Users can ask: "What was revenue in July?"

---

## 🔐 Step 11: Security & Data Governance

### Row-Level Security (RLS)

To limit data by role:

1. Go to **Model** tab
2. Create RLS rules:
   ```
   Location = USERNAME() = [Sales Manager]
   Vehicle Type = USERPRINCIPALNAME() = value in Role table
   ```

3. Test RLS in Power BI Desktop
4. Deploy and assign users to roles in Power BI Service

### Sensitivity Labels

Mark sensitive data:
- Booking_Value
- Customer_ID
- Driver_ID

---

## 📈 Performance Optimization

### Best Practices

1. **Reduce Model Size**
   - Hide unnecessary columns
   - Archive old data
   - Use aggregations for large datasets

2. **Optimize DAX**
   - Use CALCULATE efficiently
   - Avoid iterative functions
   - Create summary tables

3. **Query Folding**
   - Keep Power Query transformations simple
   - Let data source do heavy lifting

---

## 🔧 Troubleshooting

| Issue | Solution |
|---|---|
| Slow dashboard | Reduce data volume, optimize DAX, enable aggregations |
| Data not refreshing | Check refresh schedule, verify data source access |
| Slicers not working | Check interactions, verify data relationships |
| Missing data | Validate data types, check filters |
| Memory issues | Archive old data, split dashboard into multiple pages |

---

## 📚 Resources

- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [DAX Function Reference](https://dax.guide/)
- [Power BI Best Practices](https://docs.microsoft.com/en-us/power-bi/guidance/overview)

---

**Dashboard Version**: 2.0 - Interactive Analytics Dashboard
**Last Updated**: February 2026
