"""
Data Export Script for Power BI Dashboard
Exports Ola Rides data to formats compatible with Power BI
Supports: CSV, Excel, JSON, SQL INSERT statements
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import os
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'dbname': 'ola_ride_insights',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

class OlaDataExporter:
    """Export Ola rides data for Power BI dashboard"""
    
    def __init__(self, output_dir='./exported_data'):
        """Initialize exporter with output directory"""
        self.output_dir = output_dir
        self.conn = None
        self.df = None
        
        # Create output directory if not exists
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Output directory: {self.output_dir}")
    
    def connect_database(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            logger.info("✓ Connected to PostgreSQL database")
            return True
        except Exception as e:
            logger.error(f"✗ Database connection failed: {e}")
            return False
    
    def load_data(self):
        """Load July rides data from database"""
        try:
            query = 'SELECT * FROM july_rides'
            self.df = pd.read_sql_query(query, self.conn)
            
            # Convert date column
            self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')
            
            logger.info(f"✓ Loaded {len(self.df):,} records from july_rides table")
            logger.info(f"✓ Columns: {', '.join(self.df.columns)}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to load data: {e}")
            return False
    
    def export_csv(self):
        """Export data as CSV"""
        try:
            filename = os.path.join(self.output_dir, 'july_rides.csv')
            self.df.to_csv(filename, index=False)
            logger.info(f"✓ Exported to CSV: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ CSV export failed: {e}")
            return None
    
    def export_excel(self):
        """Export data as Excel with multiple sheets"""
        try:
            filename = os.path.join(self.output_dir, 'july_rides.xlsx')
            
            with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
                # Main data
                self.df.to_excel(writer, sheet_name='Raw Data', index=False)
                
                # Summary statistics
                summary = self._generate_summary()
                summary.to_excel(writer, sheet_name='Summary', index=True)
                
                # Vehicle type breakdown
                vehicle_stats = self._generate_vehicle_stats()
                vehicle_stats.to_excel(writer, sheet_name='Vehicle Stats', index=False)
                
                # Location analysis
                locations = self._generate_location_analysis()
                locations.to_excel(writer, sheet_name='Top Locations', index=False)
                
                # Payment method breakdown
                payment_stats = self._generate_payment_stats()
                payment_stats.to_excel(writer, sheet_name='Payment Methods', index=False)
                
                # Format sheets
                workbook = writer.book
                header_format = workbook.add_format({
                    'bg_color': '#4472C4',
                    'font_color': 'white',
                    'bold': True,
                    'border': 1
                })
                
                for sheet_name in writer.sheets:
                    worksheet = writer.sheets[sheet_name]
                    for col_num, value in enumerate(worksheet.table):
                        worksheet.write(0, col_num, value)
            
            logger.info(f"✓ Exported to Excel: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ Excel export failed: {e}")
            return None
    
    def export_json(self):
        """Export data as JSON for API/integration"""
        try:
            filename = os.path.join(self.output_dir, 'july_rides.json')
            
            # Convert datetime to string for JSON serialization
            df_json = self.df.copy()
            df_json['Date'] = df_json['Date'].astype(str)
            
            data = {
                'metadata': {
                    'total_records': len(self.df),
                    'export_date': datetime.now().isoformat(),
                    'columns': list(self.df.columns),
                    'data_types': {col: str(dtype) for col, dtype in self.df.dtypes.items()}
                },
                'summary': {
                    'total_rides': len(self.df),
                    'total_revenue': float(self.df['Booking_Value'].sum()),
                    'date_range': {
                        'start': str(self.df['Date'].min()),
                        'end': str(self.df['Date'].max())
                    },
                    'vehicle_types': list(self.df['Vehicle_Type'].unique()),
                    'booking_statuses': list(self.df['Booking_Status'].unique())
                },
                'data': df_json.to_dict(orient='records')
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"✓ Exported to JSON: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ JSON export failed: {e}")
            return None
    
    def export_parquet(self):
        """Export as Parquet (efficient for big data)"""
        try:
            filename = os.path.join(self.output_dir, 'july_rides.parquet')
            self.df.to_parquet(filename, index=False)
            logger.info(f"✓ Exported to Parquet: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ Parquet export failed: {e}")
            return None
    
    def _generate_summary(self):
        """Generate summary statistics"""
        summary_data = {
            'Metric': [
                'Total Rides',
                'Total Revenue (₹)',
                'Successful Rides',
                'Canceled Rides',
                'Success Rate (%)',
                'Cancellation Rate (%)',
                'Avg Revenue per Ride (₹)',
                'Avg Driver Rating',
                'Avg Customer Rating',
                'Total Distance (KM)',
                'Avg Distance per Ride (KM)',
                'Unique Customers',
                'Unique Locations'
            ],
            'Value': [
                len(self.df),
                f"{self.df['Booking_Value'].sum():,.2f}",
                len(self.df[self.df['Booking_Status'] == 'Success']),
                len(self.df[self.df['Booking_Status'] != 'Success']),
                f"{(len(self.df[self.df['Booking_Status'] == 'Success']) / len(self.df) * 100):.2f}",
                f"{(len(self.df[self.df['Booking_Status'] != 'Success']) / len(self.df) * 100):.2f}",
                f"{self.df['Booking_Value'].mean():,.2f}",
                f"{self.df['Driver_Ratings'].mean():.2f}",
                f"{self.df['Customer_Rating'].mean():.2f}",
                f"{self.df['Ride_Distance'].sum():,.2f}",
                f"{self.df['Ride_Distance'].mean():.2f}",
                self.df['Customer_ID'].nunique(),
                self.df['Pickup_Location'].nunique()
            ]
        }
        return pd.DataFrame(summary_data)
    
    def _generate_vehicle_stats(self):
        """Generate vehicle type statistics"""
        vehicle_stats = self.df.groupby('Vehicle_Type').agg({
            'Booking_ID': 'count',
            'Booking_Value': ['sum', 'mean'],
            'Driver_Ratings': 'mean',
            'Customer_Rating': 'mean',
            'Ride_Distance': 'mean'
        }).reset_index()
        
        vehicle_stats.columns = [
            'Vehicle_Type',
            'Total_Rides',
            'Total_Revenue',
            'Avg_Revenue',
            'Avg_Driver_Rating',
            'Avg_Customer_Rating',
            'Avg_Distance'
        ]
        
        return vehicle_stats.round(2)
    
    def _generate_location_analysis(self):
        """Generate top locations analysis"""
        pickup_stats = self.df['Pickup_Location'].value_counts().head(10)
        drop_stats = self.df['Drop_Location'].value_counts().head(10)
        
        locations = pd.DataFrame({
            'Pickup_Location': pickup_stats.index,
            'Pickup_Count': pickup_stats.values,
            'Drop_Location': drop_stats.index,
            'Drop_Count': drop_stats.values
        })
        
        return locations
    
    def _generate_payment_stats(self):
        """Generate payment method statistics"""
        payment_stats = self.df.groupby('Payment_Method').agg({
            'Booking_ID': 'count',
            'Booking_Value': 'sum'
        }).reset_index()
        
        payment_stats.columns = ['Payment_Method', 'Transactions', 'Total_Revenue']
        payment_stats['Percentage'] = (
            payment_stats['Total_Revenue'] / payment_stats['Total_Revenue'].sum() * 100
        )
        
        return payment_stats.round(2)
    
    def generate_data_dictionary(self):
        """Generate data dictionary for documentation"""
        try:
            filename = os.path.join(self.output_dir, 'DATA_DICTIONARY.txt')
            
            with open(filename, 'w') as f:
                f.write("OLA RIDES DATA DICTIONARY\n")
                f.write("=" * 60 + "\n\n")
                
                for column, dtype in self.df.dtypes.items():
                    f.write(f"Column: {column}\n")
                    f.write(f"Data Type: {dtype}\n")
                    f.write(f"Non-Null Count: {self.df[column].notna().sum():,}\n")
                    f.write(f"Null Count: {self.df[column].isna().sum():,}\n")
                    
                    if dtype == 'object':
                        f.write(f"Unique Values: {self.df[column].nunique()}\n")
                        f.write(f"Sample Values: {', '.join(map(str, self.df[column].unique()[:5]))}\n")
                    else:
                        f.write(f"Min: {self.df[column].min()}\n")
                        f.write(f"Max: {self.df[column].max()}\n")
                        f.write(f"Mean: {self.df[column].mean():.2f}\n")
                    
                    f.write("-" * 60 + "\n\n")
            
            logger.info(f"✓ Generated data dictionary: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ Data dictionary generation failed: {e}")
            return None
    
    def export_all(self):
        """Export data in all formats"""
        logger.info("\n" + "="*60)
        logger.info("STARTING DATA EXPORT PROCESS")
        logger.info("="*60 + "\n")
        
        if not self.connect_database():
            return False
        
        if not self.load_data():
            return False
        
        exported_files = {}
        
        # Export in various formats
        csv_file = self.export_csv()
        if csv_file:
            exported_files['CSV'] = csv_file
        
        excel_file = self.export_excel()
        if excel_file:
            exported_files['Excel'] = excel_file
        
        json_file = self.export_json()
        if json_file:
            exported_files['JSON'] = json_file
        
        try:
            parquet_file = self.export_parquet()
            if parquet_file:
                exported_files['Parquet'] = parquet_file
        except ImportError:
            logger.warning("⚠ Parquet export requires 'pyarrow' package")
        
        dict_file = self.generate_data_dictionary()
        if dict_file:
            exported_files['Dictionary'] = dict_file
        
        logger.info("\n" + "="*60)
        logger.info("EXPORT COMPLETE")
        logger.info("="*60)
        logger.info(f"\nExported Files ({len(exported_files)}):")
        for format_type, filepath in exported_files.items():
            logger.info(f"  ✓ {format_type}: {filepath}")
        
        return exported_files
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")


# Main execution
if __name__ == '__main__':
    exporter = OlaDataExporter()
    
    try:
        results = exporter.export_all()
        if results:
            print("\n✓ All exports completed successfully!")
            print(f"\nFiles saved in: {exporter.output_dir}")
    except Exception as e:
        logger.error(f"Export process failed: {e}")
    finally:
        exporter.close()
