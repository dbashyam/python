# Power BI Visualization Specifications

## 📊 Dashboard Architecture

### Page Structure (5 Pages)
1. **Executive Overview** - High-level KPIs at a glance
2. **Ride Trends & Performance** - Temporal analysis and patterns
3. **Revenue Deep Dive** - Comprehensive revenue analysis
4. **Cancellation Analysis** - Detailed failure/cancellation insights
5. **Location & Vehicle Intelligence** - Geographic and fleet analysis

---

## 🎯 PAGE 1: Executive Overview

### Layout
- **Top Row**: 6 KPI Cards (1x6)
- **Middle Row**: 2 Large Metrics (2x3) + Color Status Indicators
- **Bottom Row**: Trend Sparklines (1x3 grid)
- **Right Sidebar**: Dynamic Filter Pane

### Visualizations

#### 1. Total Rides (Card)
```
Field: [Total Rides]
Format: #,##0
Font: Bold, Size 28
Color: Blue (#4472C4)
Icon: 🚗
```

#### 2. Total Revenue (Card)
```
Field: [Total Revenue]
Format: ₹#,##0
Font: Bold, Size 28
Color: Green (#70AD47)
Icon: 💰
```

#### 3. Success Rate % (Card)
```
Field: [Success Rate]
Format: 0.0"%"
Font: Bold, Size 28
Color: Green (#70AD47)
Threshold: >90% Green, 80-90% Yellow, <80% Red
Icon: ✅
```

#### 4. Cancellation Rate % (Card)
```
Field: [Cancellation Rate]
Format: 0.0"%"
Font: Bold, Size 28
Color: Red (#C5504A)
Threshold: <10% Green, 10-15% Yellow, >15% Red
Icon: ❌
```

#### 5. Avg Driver Rating (Card)
```
Field: [Avg Driver Rating]
Format: 0.00
Font: Bold, Size 28
Color: Orange (#FFC000)
Suffix: "⭐"
Threshold: ≥4.5 Green, 4.0-4.5 Yellow, <4.0 Red
```

#### 6. Avg Customer Rating (Card)
```
Field: [Avg Customer Rating]
Format: 0.00
Font: Bold, Size 28
Color: Orange (#FFC000)
Suffix: "⭐"
Threshold: ≥4.5 Green, 4.0-4.5 Yellow, <4.0 Red
```

#### 7. Performance Gauge - Revenue
```
Type: Gauge
Value: [Total Revenue] / Target
Target: Set to 30,000,000 (₹)
Format: ₹#,##0
Color: Green (100%), Yellow (80%), Red (<80%)
Size: 300x300px
```

#### 8. Performance Gauge - Success Rate
```
Type: Gauge
Value: [Success Rate]
Target: 95%
Format: 0.0"%"
Color: Green (>95%), Yellow (90-95%), Red (<90%)
Size: 300x300px
```

#### 9. KPI Trends
```
Type: Line Chart
X-axis: Date (daily)
Y-axis: [Total Rides]
Add: Trend line
Period: Last 30 days
Color: Blue
Size: Full width, Height: 200px
```

---

## 🎯 PAGE 2: Ride Trends & Performance

### Section 1: Daily Trends (Full Width, Top)

#### 1. Daily Ride Volume
```
Type: Line Chart with Area
Title: "Daily Ride Volume"
X-axis: Date (formatted YYYY-MM-DD)
Y-axis: Count of Booking_ID
Data Series: Total Rides (Blue), Success (Green), Failed (Red)
Format: 
  - Markers: Enabled
  - Trend Line: Enabled
  - Data Labels: Enabled on series
Colors:
  - Total: #4472C4 (Blue)
  - Success: #70AD47 (Green)
  - Failed: #C5504A (Red)
Size: Full width, Height: 300px
Interaction: Filter on date range
```

#### 2. Hourly Heatmap
```
Type: Matrix/Table
Title: "Ride Volume Heatmap"
Rows: Day of Month (1-31)
Columns: Hour of Day (0-23)
Values: Count of Booking_ID
Conditional Formatting:
  - Color Scale: White → Green → Dark Green
  - Range: Min (White) to Max (Dark Green)
  - Font: White on dark backgrounds
Size: 500x400px
Interaction: Click cells to drill-through
```

#### 3. Peak Hours Analysis
```
Type: Combo Chart
Title: "Revenue & Rides by Hour"
X-axis: Hour of Day (0-23)
Column Y-axis: Count of Booking_ID (Blue bars)
Line Y-axis: Sum of Booking_Value (Orange line with markers)
Format:
  - Column: Light Blue
  - Line: Orange, Width: 2pt
  - Data Labels: Enabled on line
Size: Full width, Height: 300px
```

### Section 2: Status Trends (2 Columns)

#### 4. Booking Status Distribution
```
Type: Pie Chart
Title: "Booking Status Breakdown"
Legend: Booking_Status
Values: Count of Booking_ID
Colors:
  - Success: Green (#70AD47)
  - Canceled by Driver: Red (#C5504A)
  - Canceled by Customer: Orange (#FFC000)
  - Driver Not Found: Gray (#808080)
Data Labels: Show Category and Percentage
Size: 400x300px
```

#### 5. Status Trend Over Time
```
Type: Stacked Area Chart
Title: "Status Trend Over Time"
X-axis: Date
Y-axis: Count of Booking_ID (Stacked)
Legend: Booking_Status
Colors: Same as Status Distribution
Format:
  - Transparency: 70%
  - Markers: Enabled
Size: 400x300px
Interaction: Hover to show exact counts
```

### Section 3: Detailed Analysis (1 Row)

#### 6. Vehicle Type Performance
```
Type: Clustered Bar Chart
Title: "Performance by Vehicle Type"
Axis: Vehicle_Type
Value 1: Count of Booking_ID (Blue bars)
Value 2: [Success Rate %] (Green overlay, right Y-axis)
Format:
  - Bars: Blue
  - Line (Success %): Green
  - Data Labels: Enabled
Size: Full width, Height: 250px
Interaction: Filter on vehicle type
```

---

## 🎯 PAGE 3: Revenue Deep Dive

### Section 1: Revenue Trends (Full Width, Top)

#### 1. Daily Revenue Area Chart
```
Type: Area Chart
Title: "Daily Revenue Trend"
X-axis: Date
Y-axis: Sum of Booking_Value (₹)
Format:
  - Color: Green gradient (#70AD47 → #00B050)
  - Transparency: 50%
  - Trend Line: Enabled
  - Confidence Interval: Enabled (95%)
Data Labels: Enabled on peaks
Size: Full width, Height: 320px
Interaction: Drill-through to daily detail
```

#### 2. Revenue & Growth Rate
```
Type: Combo Chart
Title: "Revenue & Daily Growth Rate"
X-axis: Date
Column Y-axis: Daily Revenue (Green bars)
Line Y-axis: Growth Rate % (Blue line)
Format:
  - Columns: Light Green
  - Line: Blue, Width: 2pt
  - Data Labels: Growth rate labels
Size: Full width, Height: 280px
```

### Section 2: Revenue by Category (2x2 Grid)

#### 3. Revenue by Vehicle Type
```
Type: Horizontal Bar Chart
Title: "Revenue by Vehicle Type"
Axis: Vehicle_Type
Value: Sum of Booking_Value
Sort: Descending
Format:
  - Colors: Gradient (Light Blue → Dark Blue)
  - Data Labels: Show value and percentage
  - Conditional Formatting: Green (highest) → Yellow (middle) → Red (lowest)
Size: 400x300px
```

#### 4. Revenue by Payment Method
```
Type: Donut Chart
Title: "Revenue Distribution - Payment Method"
Legend: Payment_Method
Values: Sum of Booking_Value
Colors:
  - Cash: #4472C4 (Blue)
  - UPI: #ED7D31 (Orange)
  - Credit Card: #70AD47 (Green)
Data Labels: Show Category, Value, and Percentage (inside pie)
Size: 400x300px
```

#### 5. Revenue Distribution
```
Type: Histogram (Bin settings)
Title: "Booking Value Distribution"
Field: Booking_Value
Bins: 20
X-axis: Booking Value Range (₹)
Y-axis: Count of Bookings
Format:
  - Color: Light Orange (#FFC000)
  - Bin Width: 50
Overlay: Add average line (red dashed)
Size: 400x300px
```

#### 6. Top Booking Value Performers
```
Type: Table
Title: "Revenue Metrics by Vehicle Type"
Columns:
  - Vehicle_Type
  - Count of Rides
  - Total Revenue (₹)
  - Avg Revenue (₹)
  - Revenue % of Total
Sort: By Total Revenue (Descending)
Format:
  - Header: Bold, Blue background
  - Totals Row: Yes
  - Conditional Formatting on Revenue columns: Green (high) → Red (low)
Size: Full width, Height: 250px
```

### Section 3: Detailed Metrics (Full Width)

#### 7. Revenue KPI Cards (4-column row)
```
Card 1: Average Revenue per Ride
  - Value: [Avg Revenue per Ride]
  - Format: ₹0
  - Sparkline: Last 30 days
  
Card 2: Revenue per KM
  - Value: [Revenue per KM]
  - Format: ₹0.00
  - Sparkline: Last 30 days
  
Card 3: Revenue from Successful Rides
  - Value: [Revenue from Successful]
  - Format: ₹#,##0
  - Change: vs Previous 7 days
  
Card 4: Revenue Lost (Cancellations)
  - Value: [Revenue Lost]
  - Format: ₹#,##0
  - Color: Red (#C5504A)
```

---

## 🎯 PAGE 4: Cancellation Analysis

### Section 1: Status Breakdown (Top)

#### 1. Cancellation Overview Cards (4-column row)
```
Card 1: Total Canceled
  - Value: [Canceled Rides]
  - Format: #,##0
  - Color: Red
  
Card 2: Canceled by Driver
  - Value: [Canceled by Driver]
  - Format: #,##0
  - Percentage: % of total canceled
  
Card 3: Canceled by Customer
  - Value: [Canceled by Customer]
  - Format: #,##0
  - Percentage: % of total canceled
  
Card 4: Driver Not Found
  - Value: [Driver Not Found]
  - Format: #,##0
  - Color: Gray
```

#### 2. Cancellation Rates by Vehicle Type
```
Type: Bar Chart (Horizontal)
Title: "Cancellation Rate by Vehicle Type"
Axis: Vehicle_Type
Value: [Cancellation Rate %]
Format: 0.0"%"
Colors: Conditional Formatting
  - Red: >15%
  - Yellow: 10-15%
  - Green: <10%
Data Labels: Show percentage
Size: Full width, Height: 250px
Interaction: Click bar to drill down
```

### Section 2: Root Cause Analysis (2 Columns)

#### 3. Top Cancellation Reasons
```
Type: Horizontal Bar Chart
Title: "Top 10 Cancellation Reasons"
Axis: Incomplete_Rides_Reason (Top 10)
Value: Count of Booking_ID
Sort: Descending
Format:
  - Colors: Red gradient (darkest = most cancellations)
  - Data Labels: Show count and percentage
Size: 500x350px
```

#### 4. Cancellation by Status Type
```
Type: Pie Chart
Title: "Cancellation Breakdown"
Legend: Booking_Status (Canceled/Driver Not Found only)
Values: Count of Booking_ID
Colors:
  - Canceled by Driver: Dark Red (#C5504A)
  - Canceled by Customer: Orange (#FFC000)
  - Driver Not Found: Gray (#808080)
Data Labels: Show Category and Percentage
Size: 500x350px
```

### Section 3: Trends & Deep Dive

#### 5. Cancellation Trend Over Time
```
Type: Line Chart (Multi-series)
Title: "Cancellation Trend Over Time"
X-axis: Date
Y-axis: Count of Canceled Bookings
Legend: 
  - Canceled by Driver (Red line)
  - Canceled by Customer (Orange line)
  - Driver Not Found (Gray line)
Format:
  - Markers: Enabled
  - Width: 2pt
  - Trend Lines: Enabled
Data Labels: Enabled on peaks
Size: Full width, Height: 300px
```

#### 6. Cancellation Impact Table
```
Type: Table
Title: "Cancellation Impact Analysis"
Columns:
  - Booking_Status
  - Count of Rides
  - Percentage
  - Lost Revenue (₹)
  - Avg Revenue per Cancellation
Sort: By Count (Descending)
Format:
  - Conditional Formatting: Red for canceled, Green for success
  - Totals Row: Yes
Size: Full width, Height: 250px
```

---

## 🎯 PAGE 5: Location & Vehicle Intelligence

### Section 1: Geographic Analysis (2 Columns, Top)

#### 1. Top 10 Pickup Locations
```
Type: Horizontal Bar Chart
Title: "Top 10 Pickup Locations"
Axis: Pickup_Location (Top 10)
Value: Count of Booking_ID
Sort: Descending
Format:
  - Colors: Blue gradient
  - Data Labels: Show count and percentage
  - Sparkline: Mini trend per location
Size: 500x350px
Interaction: Click to filter by location
```

#### 2. Top 10 Drop Locations
```
Type: Horizontal Bar Chart
Title: "Top 10 Drop Locations"
Axis: Drop_Location (Top 10)
Value: Count of Booking_ID
Sort: Descending
Format:
  - Colors: Green gradient
  - Data Labels: Show count and percentage
Size: 500x350px
```

#### 3. Location Correlation
```
Type: Table
Title: "Top Routes (Pickup → Drop)"
Columns:
  - Pickup_Location
  - Drop_Location
  - Count of Rides
  - Avg Revenue
Sort: By Count (Descending)
Top N: 10
Format:
  - Conditional Formatting on Count: Green (high) → Yellow (middle) → Red (low)
Size: Full width, Height: 250px
```

### Section 2: Vehicle Performance (2x2 Grid)

#### 4. Vehicle Type Distribution
```
Type: Pie Chart
Title: "Rides by Vehicle Type"
Legend: Vehicle_Type
Values: Count of Booking_ID
Colors:
  - Bike: #4472C4 (Blue)
  - Mini: #ED7D31 (Orange)
  - Prime Sedan: #70AD47 (Green)
  - Prime SUV: #FFC000 (Yellow)
  - eBike: #5B9BD5 (Light Blue)
Data Labels: Show Category and Percentage
Size: 400x300px
```

#### 5. Vehicle Revenue Contribution
```
Type: Donut Chart
Title: "Revenue by Vehicle Type"
Legend: Vehicle_Type
Values: Sum of Booking_Value
Format:
  - Same colors as distribution
  - Data Labels: Show percentage (inside pie)
  - Specify total revenue in center
Size: 400x300px
```

#### 6. Vehicle Performance Scorecard
```
Type: Table
Title: "Vehicle Type Performance Metrics"
Columns:
  - Vehicle_Type
  - Total Rides (#,##0)
  - Revenue (₹#,##0)
  - Avg Revenue (₹0)
  - Avg Driver Rating (0.00⭐)
  - Avg Customer Rating (0.00⭐)
  - Cancellation Rate (0.0%)
Sort: By Total Rides (Descending)
Format:
  - Conditional Formatting on Ratings: Green (>4.5) → Yellow (4.0-4.5) → Red (<4.0)
  - Conditional Formatting on Cancel Rate: Green (<10%) → Yellow (10-15%) → Red (>15%)
Size: Full width, Height: 400px
```

---

## 🎨 FILTER PANE (All Pages)

### Recommended Slicers

#### 1. Date Range Slicer
```
Type: Date Picker (Between Range)
Field: july_rides[Date]
Default: First and Last date in dataset
Position: Top of sidebar
Width: 250px
```

#### 2. Vehicle Type Slicer
```
Type: Buttons (Multiple select)
Field: july_rides[Vehicle_Type]
Default: All selected
Position: Below date slicer
Orientation: Vertical
```

#### 3. Booking Status Slicer
```
Type: Dropdown (Single or Multiple)
Field: july_rides[Booking_Status]
Default: All
Position: Middle of sidebar
```

#### 4. Payment Method Slicer
```
Type: Buttons
Field: july_rides[Payment_Method]
Default: All
Orientation: Horizontal (2 rows)
```

#### 5. Revenue Range Slicer
```
Type: Numeric Range
Field: july_rides[Booking_Value]
Default: Min to Max
Min Value: 0
Max Value: 1000
```

#### 6. Driver Rating Slicer
```
Type: Numeric Range
Field: july_rides[Driver_Ratings]
Default: 0 to 5
Step: 0.5
```

---

## 🎨 Color Scheme & Branding

### Official Colors
```
Primary Blue: #4472C4
Success Green: #70AD47
Warning Orange: #FFC000
Error Red: #C5504A
Neutral Gray: #808080
Light Background: #F2F2F2
Dark Text: #262626
```

### Gradients
```
Blue Gradient: #4472C4 → #DEEBF7
Green Gradient: #70AD47 → #E2EFDA
Red Gradient: #C5504A → #FCE4D6
Orange Gradient: #FFC000 → #FEF5DE
```

---

## 📱 Mobile Layout Optimization

For mobile viewing on Power BI app:

1. **Page 1 (Overview)**: Stack KPI cards vertically
2. **Page 2 (Trends)**: Hide heatmap, resize charts to mobile width
3. **Page 3 (Revenue)**: Primary chart full width, others scroll
4. **Page 4 (Cancellations)**: Hide detailed table, show key metrics
5. **Page 5 (Locations)**: Hide location correlation table

---

**Visualization Specifications Version**: 2.0
**Last Updated**: February 2026
