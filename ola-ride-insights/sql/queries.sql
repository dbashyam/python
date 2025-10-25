SELECT "Date", COUNT("Booking_ID") AS ride_count
FROM july_rides
GROUP BY "Date"
ORDER BY "Date";

SELECT 
    COUNT(*) AS total_rides,
    SUM(CASE WHEN "Booking_Status" = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_rides,
    ROUND(100.0 * SUM(CASE WHEN "Booking_Status" = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancelled_pct
FROM july_rides;


SELECT 
    AVG("Driver_Ratings") AS avg_driver_rating,
    AVG("Customer_Rating") AS avg_customer_rating
FROM july_rides
WHERE "Driver_Ratings" IS NOT NULL AND "Customer_Rating" IS NOT NULL;


SELECT "Vehicle_Type", SUM("Ride_Distance") AS total_distance
FROM july_rides
GROUP BY "Vehicle_Type"
ORDER BY total_distance DESC
LIMIT 5;


SELECT "Incomplete_Rides_Reason", COUNT(*) AS count
FROM july_rides
WHERE "Booking_Status" = 'Cancelled'
GROUP BY "Incomplete_Rides_Reason"
ORDER BY count DESC;

SELECT "Payment_Method", SUM("Booking_Value") AS total_revenue
FROM july_rides
WHERE "Booking_Status" = 'Completed'
GROUP BY "Payment_Method"
ORDER BY total_revenue DESC;


SELECT 
    SUM(CASE WHEN "Booking_ID" IS NULL THEN 1 ELSE 0 END) AS null_booking_id,
    SUM(CASE WHEN "Booking_Value" IS NULL THEN 1 ELSE 0 END) AS null_booking_value,
    SUM(CASE WHEN "Ride_Distance" IS NULL THEN 1 ELSE 0 END) AS null_ride_distance
FROM july_rides;

