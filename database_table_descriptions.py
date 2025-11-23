table_description = [
  {
    "id": "DimAccount",
    "text": "Dimension: financial accounts. Columns: AccountKey, ParentAccountKey, AccountDescription, AccountType, ValueType. Hierarchy via ParentAccountKey. Used in FactFinance for financial reporting. Keywords: account, finance, hierarchy, ledger.",
    "metadata": { "table": "DimAccount" }
  },
  {
    "id": "DimCurrency",
    "text": "Dimension: currency lookup. Columns: CurrencyKey, CurrencyAlternateKey, CurrencyName. Joins: CurrencyKey→FactCurrencyRate, FactInternetSales, FactResellerSales. Keywords: currency, exchange rate, monetary.",
    "metadata": { "table": "DimCurrency" }
  },
  {
    "id": "DimCustomer",
    "text": "Dimension: customer demographics + geography. Columns: CustomerKey, GeographyKey, Name, Gender, Income, Education, Occupation, Address, BirthDate. Joins: CustomerKey→FactInternetSales, FactSurveyResponse. Keywords: customer, demographics, geography, household, consumer.",
    "metadata": { "table": "DimCustomer" }
  },
  {
    "id": "DimDate",
    "text": "Dimension: calendar date. Columns: DateKey, FullDate, Day, MonthName, MonthNumber, Quarter, Year, FiscalYear. Joins to all fact tables with DateKey, OrderDateKey, DueDateKey, ShipDateKey. Keywords: date, calendar, year, quarter, time.",
    "metadata": { "table": "DimDate" }
  },
  {
    "id": "DimDepartmentGroup",
    "text": "Dimension: department hierarchy. Columns: DepartmentGroupKey, ParentDepartmentGroupKey, DepartmentGroupName. Joins: DepartmentGroupKey→FactFinance. Keywords: department, org structure, hierarchy.",
    "metadata": { "table": "DimDepartmentGroup" }
  },
  {
    "id": "DimEmployee",
    "text": "Dimension: employee metadata. Columns: EmployeeKey, SalesTerritoryKey, Name, HireDate, BirthDate, Title, Pay, DepartmentName. Joins: EmployeeKey→FactResellerSales, FactSalesQuota. Keywords: employee, staff, salesperson, HR.",
    "metadata": { "table": "DimEmployee" }
  },
  {
    "id": "DimGeography",
    "text": "Dimension: geography lookup. Columns: GeographyKey, City, StateProvince, CountryRegion, PostalCode, SalesTerritoryKey. Joins: GeographyKey→DimCustomer, DimReseller. Keywords: geography, region, city, territory.",
    "metadata": { "table": "DimGeography" }
  },
  {
    "id": "DimOrganization",
    "text": "Dimension: organizational hierarchy. Columns: OrganizationKey, ParentOrganizationKey, OrganizationName, CurrencyKey. Joins: OrganizationKey→FactFinance. Keywords: organization, business unit, hierarchy.",
    "metadata": { "table": "DimOrganization" }
  },
  {
    "id": "DimProductCategory",
    "text": "Dimension: product category. Columns: ProductCategoryKey, EnglishProductCategoryName. Joins: ProductCategoryKey→DimProductSubcategory. Keywords: product category, product hierarchy, grouping.",
    "metadata": { "table": "DimProductCategory" }
  },
  {
    "id": "DimProductSubcategory",
    "text": "Dimension: product subcategory. Columns: ProductSubcategoryKey, ProductCategoryKey, EnglishProductSubcategoryName. Joins: ProductSubcategoryKey→DimProduct. Keywords: product subcategory, hierarchy, grouping.",
    "metadata": { "table": "DimProductSubcategory" }
  },
  {
    "id": "DimProduct",
    "text": "Dimension: product master data. Columns: ProductKey, ProductSubcategoryKey, ProductName, StandardCost, ListPrice, Color, ModelName. Joins: ProductKey→FactInternetSales, FactResellerSales, FactProductInventory. Keywords: product, item, SKU, cost, price, catalog.",
    "metadata": { "table": "DimProduct" }
  },
  {
    "id": "DimPromotion",
    "text": "Dimension: promotion metadata. Columns: PromotionKey, PromotionType, PromotionCategory, DiscountPct, StartDate, EndDate. Joins: PromotionKey→FactInternetSales, FactResellerSales. Keywords: promotion, discount, marketing campaign.",
    "metadata": { "table": "DimPromotion" }
  },
  {
    "id": "DimReseller",
    "text": "Dimension: reseller information. Columns: ResellerKey, GeographyKey, ResellerName, BusinessType, AnnualSales, NumberEmployees. Joins: ResellerKey→FactResellerSales. Keywords: reseller, B2B, wholesale, partner.",
    "metadata": { "table": "DimReseller" }
  },
  {
    "id": "DimSalesReason",
    "text": "Dimension: sales reason lookup. Columns: SalesReasonKey, SalesReasonName, SalesReasonReasonType. Joins: SalesReasonKey→FactInternetSalesReason. Keywords: sales reason, marketing, promotion reason.",
    "metadata": { "table": "DimSalesReason" }
  },
  {
    "id": "DimSalesTerritory",
    "text": "Dimension: sales territory. Columns: SalesTerritoryKey, Region, Country, Group. Joins: SalesTerritoryKey→DimGeography, DimEmployee, FactInternetSales, FactResellerSales. Keywords: sales territory, region, geography, region mapping.",
    "metadata": { "table": "DimSalesTerritory" }
  },
  {
    "id": "DimScenario",
    "text": "Dimension: financial scenario type. Columns: ScenarioKey, ScenarioName (Actual, Budget, Forecast). Joins: ScenarioKey→FactFinance. Keywords: scenario, actual, budget, forecast.",
    "metadata": { "table": "DimScenario" }
  },
  {
    "id": "FactAdditionalInternationalProductDescription",
    "text": "Fact: multilingual product descriptions. Columns: ProductKey, CultureName, ProductDescription. Joins: ProductKey→DimProduct. Keywords: product description, translations, internationalization, culture.",
    "metadata": { "table": "FactAdditionalInternationalProductDescription" }
  },
  {
    "id": "FactCallCenter",
    "text": "Fact: call center performance. Columns: DateKey, WageType, Shift, Operators, Calls, Orders, IssuesRaised, ServiceGrade. Joins: DateKey→DimDate. Keywords: call center, operations, performance metrics, agents, calls.",
    "metadata": { "table": "FactCallCenter" }
  },
  {
    "id": "FactCurrencyRate",
    "text": "Fact: daily currency rates. Columns: CurrencyKey, DateKey, AverageRate, EndOfDayRate. Joins: CurrencyKey→DimCurrency, DateKey→DimDate. Keywords: currency rate, forex, exchange rate, financial.",
    "metadata": { "table": "FactCurrencyRate" }
  },
  {
    "id": "FactFinance",
    "text": "Fact: financial amounts. Columns: DateKey, OrganizationKey, DepartmentGroupKey, ScenarioKey, AccountKey, Amount. Joins: DimAccount, DimDate, DimDepartmentGroup, DimOrganization, DimScenario. Keywords: finance, ledger, amount, budget, actuals.",
    "metadata": { "table": "FactFinance" }
  },
  {
    "id": "FactInternetSalesReason",
    "text": "Fact: internet sales reasons. Columns: SalesOrderNumber, SalesOrderLineNumber, SalesReasonKey. Joins: SalesReasonKey→DimSalesReason, SalesOrderNumber→FactInternetSales. Keywords: internet sales, sales reason, order reason mapping.",
    "metadata": { "table": "FactInternetSalesReason" }
  },
  {
    "id": "FactInternetSales",
    "text": "Fact: internet sales transactions. Columns: ProductKey, CustomerKey, OrderDateKey, DueDateKey, ShipDateKey, PromotionKey, CurrencyKey, SalesTerritoryKey, OrderQuantity, UnitPrice, SalesAmount, TaxAmt, Freight. Joins: DimProduct, DimCustomer, DimDate (3×), DimPromotion, DimSalesTerritory, DimCurrency. Keywords: e-commerce, internet sales, revenue, customer sales, online orders.",
    "metadata": { "table": "FactInternetSales" }
  },
  {
    "id": "FactProductInventory",
    "text": "Fact: product inventory movements. Columns: ProductKey, DateKey, MovementDate, UnitCost, UnitsIn, UnitsOut, UnitsBalance. Joins: ProductKey→DimProduct, DateKey→DimDate. Keywords: inventory, stock, warehouse, product balance.",
    "metadata": { "table": "FactProductInventory" }
  },
  {
    "id": "FactResellerSales",
    "text": "Fact: reseller (B2B) sales transactions. Columns: ProductKey, ResellerKey, EmployeeKey, PromotionKey, CurrencyKey, SalesTerritoryKey, OrderQuantity, UnitPrice, SalesAmount, TaxAmt, Freight. Joins: DimReseller, DimEmployee, DimProduct, DimPromotion, DimCurrency, DimSalesTerritory, DimDate. Keywords: reseller sales, B2B sales, wholesale, distributor revenue.",
    "metadata": { "table": "FactResellerSales" }
  },
  {
    "id": "FactSalesQuota",
    "text": "Fact: sales quotas assigned to employees. Columns: EmployeeKey, DateKey, CalendarYear, CalendarQuarter, SalesAmountQuota. Joins: EmployeeKey→DimEmployee, DateKey→DimDate. Keywords: sales quota, target, employee target, KPI.",
    "metadata": { "table": "FactSalesQuota" }
  },
  {
    "id": "FactSurveyResponse",
    "text": "Fact: customer survey responses by product category. Columns: DateKey, CustomerKey, ProductCategoryKey, ProductSubcategoryKey. Joins: CustomerKey→DimCustomer, DateKey→DimDate. Keywords: survey, customer feedback, sentiment, product category survey.",
    "metadata": { "table": "FactSurveyResponse" }
  },
  {
    "id": "NewFactCurrencyRate",
    "text": "Fact: alternate currency rate feed. Columns: CurrencyID, CurrencyDate, AverageRate, EndOfDayRate, CurrencyKey, DateKey. Joins: CurrencyKey→DimCurrency, DateKey→DimDate. Keywords: currency rate, financial feed, exchange rate history.",
    "metadata": { "table": "NewFactCurrencyRate" }
  },
  {
    "id": "ProspectiveBuyer",
    "text": "Dimension-like table: prospective buyer demographics. Columns: ProspectAlternateKey, Name, Gender, Income, Education, Occupation, City, State, Phone. Used for marketing or lead analysis. Keywords: prospective buyer, marketing lead, demographics.",
    "metadata": { "table": "ProspectiveBuyer" }
  },
  {
    "id": "AdventureWorksDWBuildVersion",
    "text": "System table: data warehouse build version. Columns: DBVersion, VersionDate. No analytic joins. Keywords: build version, metadata, system info.",
    "metadata": { "table": "AdventureWorksDWBuildVersion" }
  },
  {
    "id": "DatabaseLog",
    "text": "System table: SQL Server database log entries. Columns: DatabaseLogID, PostTime, TSQL, XmlEvent. Not used for BI queries. Keywords: database log, ddl events, audit log.",
    "metadata": { "table": "DatabaseLog" }
  },
  {
    "id": "sysdiagrams",
    "text": "System table: stores diagram definitions created in SQL Server Management Studio. Columns: diagram_id, definition. Not used for analytics. Keywords: diagrams, system metadata.",
    "metadata": { "table": "sysdiagrams" }
  }
]
