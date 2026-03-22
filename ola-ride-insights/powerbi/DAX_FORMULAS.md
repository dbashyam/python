# Power BI DAX Formulas for Ola Rides Dashboard

## 📌 Overview
This document contains all DAX formulas needed for the Ola Rides Analytics Dashboard.

---

## 📊 KPI Measures

### Total Rides
```dax
Total Rides = COUNTA('july_rides'[Booking_ID])
```

### Total Revenue (₹)
```dax
Total Revenue = SUM('july_rides'[Booking_Value])
```

### Successful Rides
```dax
Successful Rides = CALCULATE(
    COUNTA('july_rides'[Booking_ID]),
    'july_rides'[Booking_Status] = "Success"
)
```

### Canceled Rides
```dax
Canceled Rides = CALCULATE(
    COUNTA('july_rides'[Booking_ID]),
    'july_rides'[Booking_Status] <> "Success"
)
```

### Cancellation Rate (%)
```dax
Cancellation Rate = 
DIVIDE(
    [Canceled Rides],
    [Total Rides],
    0
) * 100
```

### Success Rate (%)
```dax
Success Rate = 
DIVIDE(
    [Successful Rides],
    [Total Rides],
    0
) * 100
```

### Driver Not Found Count
```dax
Driver Not Found = CALCULATE(
    COUNTA('july_rides'[Booking_ID]),
    'july_rides'[Booking_Status] = "Driver Not Found"
)
```

---

## 💰 Revenue Measures

### Average Revenue per Ride
```dax
Avg Revenue per Ride = 
DIVIDE(
    [Total Revenue],
    [Total Rides],
    0
)
```

### Revenue per KM
```dax
Revenue per KM = 
DIVIDE(
    [Total Revenue],
    SUM('july_rides'[Ride_Distance]),
    0
)
```

### Revenue by Hour (Dynamic)
```dax
Revenue by Hour = 
CALCULATE(
    SUM('july_rides'[Booking_Value]),
    'july_rides'[Hour] = SELECTEDVALUE('july_rides'[Hour])
)
```

### Total Revenue - Success Only
```dax
Revenue from Successful = CALCULATE(
    SUM('july_rides'[Booking_Value]),
    'july_rides'[Booking_Status] = "Success"
)
```

### Revenue Lost (Cancellations)
```dax
Revenue Lost = [Total Revenue] - [Revenue from Successful]
```

---

## ⭐ Rating & Quality Measures

### Average Driver Rating
```dax
Avg Driver Rating = 
CALCULATE(
    AVERAGE('july_rides'[Driver_Ratings]),
    'july_rides'[Driver_Ratings] > 0
)
```

### Average Customer Rating
```dax
Avg Customer Rating = 
CALCULATE(
    AVERAGE('july_rides'[Customer_Rating]),
    'july_rides'[Customer_Rating] > 0
)
```

### Rides with Perfect Driver Rating (5.0)
```dax
Perfect Driver Rating = CALCULATE(
    COUNTA('july_rides'[Booking_ID]),
    'july_rides'[Driver_Ratings] = 5.0
)
```

### Rides with Perfect Customer Rating (5.0)
```dax
Perfect Customer Rating = CALCULATE(
    COUNTA('july_rides'[Booking_ID]),
    'july_rides'[Customer_Rating] = 5.0
)
```

### Low Driver Rating Count (<3.0)
```dax
Low Driver Ratings = CALCULATE(
    COUNTA('july_rides'[Booking_ID]),
    'july_rides'[Driver_Ratings] < 3.0
)
```

---

## 📏 Distance & Time Measures

### Average Ride Distance (KM)
```dax
Avg Ride Distance = AVERAGE('july_rides'[Ride_Distance])
```

### Total Distance Covered (KM)
```dax
Total Distance = SUM('july_rides'[Ride_Distance])
```

### Longest Ride Distance
```dax
Max Ride Distance = MAX('july_rides'[Ride_Distance])
```

### Shortest Ride Distance
```dax
Min Ride Distance = MINX(
    VALUES('july_rides'[Ride_Distance]),
    'july_rides'[Ride_Distance]
)
```

---

## 🅿️ Payment Method Measures

### Cash Revenue
```dax
Revenue - Cash = CALCULATE(
    SUM('july_rides'[Booking_Value]),
    'july_rides'[Payment_Method] = "Cash"
)
```

### UPI Revenue
```dax
Revenue - UPI = CALCULATE(
    SUM('july_rides'[Booking_Value]),
    'july_rides'[Payment_Method] = "UPI"
)
```

### Card Revenue
```dax
Revenue - Credit Card = CALCULATE(
    SUM('july_rides'[Booking_Value]),
    'july_rides'[Payment_Method] = "Credit Card"
)
```

### Cash Payment Percentage
```dax
Cash % = 
DIVIDE(
    [Revenue - Cash],
    [Total Revenue],
    0
) * 100
```

---

## 🚗 Vehicle Type Measures

### Rides by Vehicle Type (Formula for use in visual)
```dax
Rides - Vehicle Type = CALCULATE(
    COUNTA('july_rides'[Booking_ID]),
    'july_rides'[Vehicle_Type] = SELECTEDVALUE('july_rides'[Vehicle_Type])
)
```

### Revenue - Bike
```dax
Revenue - Bike = CALCULATE(
    SUM('july_rides'[Booking_Value]),
    'july_rides'[Vehicle_Type] = "Bike"
)
```

### Revenue - Mini
```dax
Revenue - Mini = CALCULATE(
    SUM('july_rides'[Booking_Value]),
    'july_rides'[Vehicle_Type] = "Mini"
)
```

### Revenue - Prime
```dax
Revenue - Prime = CALCULATE(
    SUM('july_rides'[Booking_Value]),
    'july_rides'[Vehicle_Type] = "Prime Sedan"
)
```

---

## 📍 Location Measures

### Unique Pickup Locations
```dax
Unique Pickup Locations = DISTINCTCOUNT('july_rides'[Pickup_Location])
```

### Unique Drop Locations
```dax
Unique Drop Locations = DISTINCTCOUNT('july_rides'[Drop_Location])
```

### Top Pickup Location
```dax
Top Pickup Location = 
MAXX(
    TOPN(1, VALUES('july_rides'[Pickup_Location])),
    [Total Rides]
)
```

---

## 📅 Time-Based Measures

### Rides by Hour of Day
```dax
Rides by Hour = CALCULATE(
    COUNTA('july_rides'[Booking_ID]),
    'july_rides'[Hour] = SELECTEDVALUE('july_rides'[Hour])
)
```

### Peak Hour Rides
```dax
Peak Hour Rides = 
MAXX(
    VALUES('july_rides'[Hour]),
    [Rides by Hour]
)
```

### Total Days in Filter
```dax
Days in Filter = 
CALCULATE(
    DISTINCTCOUNT(INT('july_rides'[Date])),
    REMOVEFILTERS('july_rides'[Hour])
)
```

### Average Rides per Day
```dax
Avg Rides per Day = 
DIVIDE(
    [Total Rides],
    [Days in Filter],
    0
)
```

---

## 🔴 Cancellation Analysis

### Canceled by Driver
```dax
Canceled by Driver = CALCULATE(
    COUNTA('july_rides'[Booking_ID]),
    'july_rides'[Booking_Status] = "Canceled by Driver"
)
```

### Canceled by Customer
```dax
Canceled by Customer = CALCULATE(
    COUNTA('july_rides'[Booking_ID]),
    'july_rides'[Booking_Status] = "Canceled by Customer"
)
```

### Top Cancellation Reason
```dax
Top Cancellation Reason = 
MAXX(
    TOPN(1, VALUES('july_rides'[Incomplete_Rides_Reason])),
    [Canceled Rides]
)
```

### Cancellation Rate by Vehicle Type
```dax
Cancellation Rate by Vehicle = 
DIVIDE(
    CALCULATE(
        COUNTA('july_rides'[Booking_ID]),
        'july_rides'[Booking_Status] <> "Success"
    ),
    COUNTA('july_rides'[Booking_ID]),
    0
) * 100
```

---

## 🔄 Running Totals & Comparisons

### Running Total Revenue (by Date)
```dax
Running Total Revenue = 
CALCULATE(
    [Total Revenue],
    FILTER(
        ALL('july_rides'[Date]),
        'july_rides'[Date] <= MAX('july_rides'[Date])
    )
)
```

### Revenue Growth (vs Previous Day)
```dax
Revenue Growth = 
DIVIDE(
    [Total Revenue] - CALCULATE(
        [Total Revenue],
        DATEADD('july_rides'[Date], -1, DAY)
    ),
    CALCULATE(
        [Total Revenue],
        DATEADD('july_rides'[Date], -1, DAY)
    ),
    0
) * 100
```

### Same Day Previous Week
```dax
Revenue - Previous Week = 
CALCULATE(
    [Total Revenue],
    DATEADD('july_rides'[Date], -7, DAY)
)
```

---

## 📊 Advanced Analytics

### Rides Above Average
```dax
Above Avg Revenue = CALCULATE(
    COUNTA('july_rides'[Booking_ID]),
    'july_rides'[Booking_Value] > [Avg Revenue per Ride]
)
```

### Customer Retention Rate
```dax
Customer Retention = 
DIVIDE(
    DISTINCTCOUNT('july_rides'[Customer_ID]),
    COUNTA('july_rides'[Booking_ID]),
    0
) * 100
```

### Revenue per Unique Customer
```dax
Revenue per Customer = 
DIVIDE(
    [Total Revenue],
    DISTINCTCOUNT('july_rides'[Customer_ID]),
    0
)
```

### Booking Conversion Rate
```dax
Conversion Rate = 
DIVIDE(
    [Successful Rides],
    [Total Rides],
    0
) * 100
```

---

## 🎨 Formatting Measures

### Revenue Formatted
```dax
Revenue Formatted = 
FORMAT([Total Revenue], "₹#,##0")
```

### Percentage Formatted
```dax
Cancellation Rate % = 
FORMAT([Cancellation Rate], "0.00%")
```

### Rating Formatted
```dax
Avg Rating Formatted = 
FORMAT([Avg Driver Rating], "0.00⭐")
```

---

## 🔢 Helper Calculated Columns (Add to Table)

### Period (Month-Week)
```dax
Period = 
"W" & WEEKNUM('july_rides'[Date]) & " " & MONTH('july_rides'[Date])
```

### Day Name
```dax
Day Name = FORMAT('july_rides'[Date], "dddd")
```

### Hour Formatted
```dax
Hour Time = 
IF(
    'july_rides'[Hour] = 0,
    "12 AM",
    IF(
        'july_rides'[Hour] < 12,
        FORMAT('july_rides'[Hour], "0") & " AM",
        IF(
            'july_rides'[Hour] = 12,
            "12 PM",
            FORMAT('july_rides'[Hour] - 12, "0") & " PM"
        )
    )
)
```

### Revenue Category
```dax
Revenue Category = 
IF(
    'july_rides'[Booking_Value] < 200, "Low",
    IF(
        'july_rides'[Booking_Value] < 400, "Medium",
        IF(
            'july_rides'[Booking_Value] < 600, "High",
            "Premium"
        )
    )
)
```

### Distance Category
```dax
Distance Category = 
IF(
    'july_rides'[Ride_Distance] < 20, "Short",
    IF(
        'july_rides'[Ride_Distance] < 40, "Medium",
        "Long"
    )
)
```

---

## 📈 Conditional Formatting Rules

### Traffic Light Status
```dax
Status Color = 
SWITCH(
    TRUE(),
    [Cancellation Rate] > 15, "Red",
    [Cancellation Rate] > 10, "Yellow",
    "Green"
)
```

### Performance Badge
```dax
Performance = 
SWITCH(
    TRUE(),
    [Avg Driver Rating] >= 4.7, "Excellent",
    [Avg Driver Rating] >= 4.5, "Very Good",
    [Avg Driver Rating] >= 4.0, "Good",
    "Needs Improvement"
)
```

---

**DAX Formula Guide Version**: 2.0
**Last Updated**: February 2026
**Total Formulas**: 60+
