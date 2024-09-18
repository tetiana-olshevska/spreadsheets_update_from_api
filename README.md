# Spreadsheets update from API

The task was to get exchange rates from API of choice (mine was - https://api.privatbank.ua/p24api/exchange_rates?json as you can access archive data). Then theese exchange rates should be uploaded to Google Spreadsheets and updated due to dates that user may enter. 

So, with this application user enters any date period and gets exchange rates in desired Google Spreadsheet by columns:
* Date
* Currency
* Sale Rate NB - Sale rate of National Bank of Ukraine
* Purchase Rate NB - Purchase rate of National Bank of Ukraine
* Sale Rate - Sale rate of Privatbank
* Purchase Rate - Purchase rate of Privatbank

If fields for date values `update_to` and `update_from` are not specified by user, they are set to current date by default.
