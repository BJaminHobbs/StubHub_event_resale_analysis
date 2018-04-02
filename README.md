# StubHub_event_resale_analysis
Program will track the "sold" tickets from StubHub (SH) via their API (https://developer.stubhub.com/store). Sold tickets are defined here as listed tickets that have left the market and have not returned.

For each event, program will output a dataframe of sold tickets, a dataframe of the remaning tickets when the program stopped, and a dataframe of tickets that left the SH market but had re-entered the market or are suspected to have re-entered the market. The dataframe of sold tickets includes statistics of the event's market when the tickets were sold. The dataframe of the remaining tickets is the last call to the SH API when the program stops with the same statistics, currently set to 1day before the event date. The dataframe of tickets that have re-entered the SH market are identified by ticket seat number. If ticket seat numbers are not available, these tickets are identified by the quantity of tickets within a row meeting or exceeding the quanity of tickets at the time of sale within that same row, within 7 days. The re-entered dataframe maintains the statistics for when tickets were first sold. 

As written, a folder 'events' must exist in the working directory.

## Routines
### Data_Mine
The main routine. 

1) Logs into SH API (API_Login)
2) Populates dict for events of choice (Mined_Events)
3) Requests market information for each event (Inv_Get)
4) Extracts key data elements from market (SH_EventParse)
5) Converts market data to dataframe, adding key statistics (LS_Stats) and saves market data (Pickle_Save)
6) Loads prior call of market dataframe for comparison (Pickle_Load)
7) Detects if any listings on the market have left or reduced quantity since the prior call. Adds those tickets listings to the event ledger (Sale_Detect)
8) Determines if tickets have re-entered the market by comparison to the existing event ledger. Removing identified leger sales and adding to the re-entered dataframe (Sale_Valid)
9) Saves event ledger and re-entered dataframe (Pickle_Save)

#### SH_API
API Login function must be supplied SH Key, SH Token, username and password. Returns login response.

Inv_Get function returns all event listings whose ticket quantity >=2 using the  login response and SH eventId.

### Mined_Events
Dict of events to be called from SH API.

### SH_EventParse
SH_EventParse function extracts key data from event market listings. Creates other key identifiers from event market listings.

LS_Stats converts event market listings to dataframe and calculates other key statistics.

LS_Days calculates how long each ticket listing has been on the market.

### Event_Pickle
Pickle_Save saves event dataframes to flat files in /event/ directory.

Pickle_Load loads event dataframes from /event/ directory.

### Sale
Sale_Detect will detect tickets that have left the SH market by comparison to the last SH API. Listings in the last call that do not appear on the market are assumed sold. Listings who have reduced the quanitity of tickets available are also assumed sold. All sold listings are added to the ledger.

Sale_Valid will compare the existing ledger to the current event market. If the seats of a prior sale return to the market, that sale is removed from the ledger and added to the re-entered dataframe. Not all ticket listings identify their seats. Within 7 days from the time of sale, if the quantity of tickets available in a given row becomes >= the quantity of tickets available in that row, those sold tickets are assumed to have re-entered the market. The 7 day window was developed from a single event showing false sales within that timeframe.

## Data Mined
### All dataframes
'currentPrice'	:	Price per ticket with fees
'listingPrice'	:	Price per ticket                                                
'quantity'	:	Quantity of available tickets listed                                
'row'	:	Row of tickets                                                          
'rowId'	:	Unique Section Number  - Row identifier                                 
'row_num'	:	Numeric row of tickets                                              
'rowId_sum'	:	Sum of available tickets in row                                     
'seats'	:	T/F if seats are listed                                                 
'seats_ls'	:	Listed seats                                                        
'sectionName'	:	SH Section Name                                                 
'section_num'	:	Section Number                                                  
'zoneName'	:	SH Zone Name                                                        
'sec_sum'	:	Sum of available tickets in section                                 
'sec_mean'	:	Mean currentPrice of listings available in section                  
'sec_med'	:	Median currentPrice of listings available in section                
'sec_std'	:	Standard deviation of currentPrice of listings available in section 
'sec_iqr'	:	IQR of currentPrice of listings available in section                
'sec_25th'	:	Lower 25% of currentPrice of listings available in section          
'sec_75th'	:	Upper 25% of currentPrice of listings available in section          
'sec_wmean'	:	Mean currentPrice of tickets available in section                   
'zone_sum'	:	Sum of available tickets in zone                                    
'zone_mean'	:	Mean currentPrice of listings available in zone                     
'zone_med'	:	Median currentPrice of listings available in zone                   
'zone_std'	:	Standard deviation of currentPrice of listings available in zone    
'zone_iqr'	:	IQR of currentPrice of listings available in zone                   
'zone_25th'	:	Lower 25% of currentPrice of listings available in zone             
'zone_75th'	:	Upper 25% of currentPrice of listings available in zone             
'zone_wmean'	:	Mean currentPrice of tickets available in zone                  


### Ledger and re-entered dataframes
'ts_ls'	:	Time tickets had been on the market                                     
'seats_sold'	:	Number of tickets sold                                          
'ts_sale'	:	Time when tickets left the market                                   
'gameover'	:	Time of the event                                                   
'days_rem'	:	Days remaining until event at at time of sale
