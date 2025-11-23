examples = [
  {
    "input": "Top 5 resellers by total reseller sales amount",
    "query": "SELECT TOP 5 DimReseller.ResellerName AS ResellerName, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimReseller ON FactResellerSales.ResellerKey = DimReseller.ResellerKey GROUP BY DimReseller.ResellerName ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 customers by total internet sales",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 products by internet sales revenue",
    "query": "SELECT TOP 10 DimProduct.EnglishProductName AS ProductName, SUM(FactInternetSales.SalesAmount) AS TotalRevenue FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.EnglishProductName ORDER BY TotalRevenue DESC"
  },
  {
    "input": "Top 5 sales territories by internet sales amount",
    "query": "SELECT TOP 5 DimSalesTerritory.SalesTerritoryRegion AS Region, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimSalesTerritory ON FactInternetSales.SalesTerritoryKey = DimSalesTerritory.SalesTerritoryKey GROUP BY DimSalesTerritory.SalesTerritoryRegion ORDER BY TotalSales DESC"
  },
  {
    "input": "Internet sales by calendar year",
    "query": "SELECT DimDate.CalendarYear AS CalendarYear, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimDate ON FactInternetSales.OrderDateKey = DimDate.DateKey GROUP BY DimDate.CalendarYear ORDER BY CalendarYear"
  },
  {
    "input": "Top 5 highest earning customers by yearly income",
    "query": "SELECT TOP 5 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, DimCustomer.YearlyIncome AS YearlyIncome FROM DimCustomer ORDER BY DimCustomer.YearlyIncome DESC"
  },
  {
    "input": "Number of customers grouped by gender",
    "query": "SELECT Gender, COUNT(*) AS TotalCustomers FROM DimCustomer GROUP BY Gender"
  },
  {
    "input": "Top 10 products with the highest inventory balance",
    "query": "SELECT TOP 10 DimProduct.EnglishProductName AS ProductName, SUM(FactProductInventory.UnitsBalance) AS TotalUnits FROM FactProductInventory INNER JOIN DimProduct ON FactProductInventory.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.EnglishProductName ORDER BY TotalUnits DESC"
  },
  {
    "input": "Top 5 employees by total reseller sales amount",
    "query": "SELECT TOP 5 DimEmployee.FirstName + ' ' + DimEmployee.LastName AS EmployeeName, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimEmployee ON FactResellerSales.EmployeeKey = DimEmployee.EmployeeKey GROUP BY DimEmployee.FirstName + ' ' + DimEmployee.LastName ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 5 dates with highest total call center calls",
    "query": "SELECT TOP 5 DimDate.FullDateAlternateKey AS Date, SUM(FactCallCenter.Calls) AS TotalCalls FROM FactCallCenter INNER JOIN DimDate ON FactCallCenter.DateKey = DimDate.DateKey GROUP BY DimDate.FullDateAlternateKey ORDER BY TotalCalls DESC"
  },
  {
    "input": "Top 5 promotions with highest discount percentage",
    "query": "SELECT TOP 5 EnglishPromotionName AS PromotionName, DiscountPct AS DiscountPercentage FROM DimPromotion ORDER BY DiscountPct DESC"
  },
  {
    "input": "Top 5 product subcategories by number of survey responses",
    "query": "SELECT TOP 5 DimProductSubcategory.EnglishProductSubcategoryName AS SubcategoryName, COUNT(*) AS TotalResponses FROM FactSurveyResponse INNER JOIN DimProductSubcategory ON FactSurveyResponse.ProductSubcategoryKey = DimProductSubcategory.ProductSubcategoryKey GROUP BY DimProductSubcategory.EnglishProductSubcategoryName ORDER BY TotalResponses DESC"
  },
  {
    "input": "Currency with the highest recorded end of day rate",
    "query": "SELECT TOP 1 DimCurrency.CurrencyName AS CurrencyName, FactCurrencyRate.EndOfDayRate AS EndOfDayRate FROM FactCurrencyRate INNER JOIN DimCurrency ON FactCurrencyRate.CurrencyKey = DimCurrency.CurrencyKey ORDER BY EndOfDayRate DESC"
  },
  {
    "input": "Top 10 departments by total finance amount",
    "query": "SELECT TOP 10 DimDepartmentGroup.DepartmentGroupName AS DepartmentName, SUM(FactFinance.Amount) AS TotalAmount FROM FactFinance INNER JOIN DimDepartmentGroup ON FactFinance.DepartmentGroupKey = DimDepartmentGroup.DepartmentGroupKey GROUP BY DimDepartmentGroup.DepartmentGroupName ORDER BY TotalAmount DESC"
  },
  {
    "input": "Top 5 organizations by finance amount",
    "query": "SELECT TOP 5 DimOrganization.OrganizationName AS OrganizationName, SUM(FactFinance.Amount) AS TotalAmount FROM FactFinance INNER JOIN DimOrganization ON FactFinance.OrganizationKey = DimOrganization.OrganizationKey GROUP BY DimOrganization.OrganizationName ORDER BY TotalAmount DESC"
  },
  {
    "input": "Top 5 employees based on number of reseller sales transactions",
    "query": "SELECT TOP 5 DimEmployee.FirstName + ' ' + DimEmployee.LastName AS EmployeeName, COUNT(*) AS TotalTransactions FROM FactResellerSales INNER JOIN DimEmployee ON FactResellerSales.EmployeeKey = DimEmployee.EmployeeKey GROUP BY DimEmployee.FirstName + ' ' + DimEmployee.LastName ORDER BY TotalTransactions DESC"
  },
  {
    "input": "Year with the highest total internet sales amount",
    "query": "SELECT TOP 1 DimDate.CalendarYear AS CalendarYear, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimDate ON FactInternetSales.OrderDateKey = DimDate.DateKey GROUP BY DimDate.CalendarYear ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 5 sales reasons used in internet sales",
    "query": "SELECT TOP 5 DimSalesReason.SalesReasonName AS SalesReason, COUNT(*) AS UsageCount FROM FactInternetSalesReason INNER JOIN DimSalesReason ON FactInternetSalesReason.SalesReasonKey = DimSalesReason.SalesReasonKey GROUP BY DimSalesReason.SalesReasonName ORDER BY UsageCount DESC"
  },
  {
    "input": "Top 10 products by total product standard cost in internet sales",
    "query": "SELECT TOP 10 DimProduct.EnglishProductName AS ProductName, SUM(FactInternetSales.ProductStandardCost) AS TotalCost FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.EnglishProductName ORDER BY TotalCost DESC"
  },
  {
    "input": "Top 5 cities with the most customers",
    "query": "SELECT TOP 5 DimGeography.City AS City, COUNT(*) AS TotalCustomers FROM DimCustomer INNER JOIN DimGeography ON DimCustomer.GeographyKey = DimGeography.GeographyKey GROUP BY DimGeography.City ORDER BY TotalCustomers DESC"
  },
  {
    "input": "Top 10 products by total reseller sales revenue",
    "query": "SELECT TOP 10 DimProduct.EnglishProductName AS ProductName, SUM(FactResellerSales.SalesAmount) AS TotalRevenue FROM FactResellerSales INNER JOIN DimProduct ON FactResellerSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.EnglishProductName ORDER BY TotalRevenue DESC"
  },
  {
    "input": "Top 10 customers by total internet sales including tax",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, SUM(FactInternetSales.SalesAmount + FactInternetSales.TaxAmt) AS TotalSalesWithTax FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY TotalSalesWithTax DESC"
  },
  {
    "input": "Top 5 promotions contributing most to internet sales",
    "query": "SELECT TOP 5 DimPromotion.EnglishPromotionName AS PromotionName, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimPromotion ON FactInternetSales.PromotionKey = DimPromotion.PromotionKey GROUP BY DimPromotion.EnglishPromotionName ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 sales territories by reseller sales",
    "query": "SELECT TOP 10 DimSalesTerritory.SalesTerritoryRegion AS Region, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimSalesTerritory ON FactResellerSales.SalesTerritoryKey = DimSalesTerritory.SalesTerritoryKey GROUP BY DimSalesTerritory.SalesTerritoryRegion ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 5 employees by total sales quota amount",
    "query": "SELECT TOP 5 DimEmployee.FirstName + ' ' + DimEmployee.LastName AS EmployeeName, SUM(FactSalesQuota.SalesAmountQuota) AS TotalQuota FROM FactSalesQuota INNER JOIN DimEmployee ON FactSalesQuota.EmployeeKey = DimEmployee.EmployeeKey GROUP BY DimEmployee.FirstName + ' ' + DimEmployee.LastName ORDER BY TotalQuota DESC"
  },
  {
    "input": "Top 5 countries by total number of customers",
    "query": "SELECT TOP 5 DimGeography.EnglishCountryRegionName AS CountryName, COUNT(*) AS TotalCustomers FROM DimCustomer INNER JOIN DimGeography ON DimCustomer.GeographyKey = DimGeography.GeographyKey GROUP BY DimGeography.EnglishCountryRegionName ORDER BY TotalCustomers DESC"
  },
  {
    "input": "Top 10 dates with highest internet order quantity",
    "query": "SELECT TOP 10 DimDate.FullDateAlternateKey AS OrderDate, SUM(FactInternetSales.OrderQuantity) AS TotalQuantity FROM FactInternetSales INNER JOIN DimDate ON FactInternetSales.OrderDateKey = DimDate.DateKey GROUP BY DimDate.FullDateAlternateKey ORDER BY TotalQuantity DESC"
  },
  {
    "input": "Top 5 product subcategories by total internet sales",
    "query": "SELECT TOP 5 DimProductSubcategory.EnglishProductSubcategoryName AS SubcategoryName, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey INNER JOIN DimProductSubcategory ON DimProduct.ProductSubcategoryKey = DimProductSubcategory.ProductSubcategoryKey GROUP BY DimProductSubcategory.EnglishProductSubcategoryName ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 5 product categories by reseller sales",
    "query": "SELECT TOP 5 DimProductCategory.EnglishProductCategoryName AS CategoryName, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimProduct ON FactResellerSales.ProductKey = DimProduct.ProductKey INNER JOIN DimProductSubcategory ON DimProduct.ProductSubcategoryKey = DimProductSubcategory.ProductSubcategoryKey INNER JOIN DimProductCategory ON DimProductSubcategory.ProductCategoryKey = DimProductCategory.ProductCategoryKey GROUP BY DimProductCategory.EnglishProductCategoryName ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 products by total freight cost in internet sales",
    "query": "SELECT TOP 10 DimProduct.EnglishProductName AS ProductName, SUM(FactInternetSales.Freight) AS TotalFreight FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.EnglishProductName ORDER BY TotalFreight DESC"
  },
  {
    "input": "Top 10 currencies by total number of currency rate entries",
    "query": "SELECT TOP 10 DimCurrency.CurrencyName AS CurrencyName, COUNT(*) AS EntryCount FROM FactCurrencyRate INNER JOIN DimCurrency ON FactCurrencyRate.CurrencyKey = DimCurrency.CurrencyKey GROUP BY DimCurrency.CurrencyName ORDER BY EntryCount DESC"
  },
  {
    "input": "Top 5 call center shifts by total number of calls handled",
    "query": "SELECT TOP 5 FactCallCenter.Shift AS ShiftName, SUM(FactCallCenter.Calls) AS TotalCalls FROM FactCallCenter GROUP BY FactCallCenter.Shift ORDER BY TotalCalls DESC"
  },
  {
    "input": "Top 5 organizations by total finance amount for Actual scenario",
    "query": "SELECT TOP 5 DimOrganization.OrganizationName AS OrganizationName, SUM(FactFinance.Amount) AS TotalAmount FROM FactFinance INNER JOIN DimOrganization ON FactFinance.OrganizationKey = DimOrganization.OrganizationKey INNER JOIN DimScenario ON FactFinance.ScenarioKey = DimScenario.ScenarioKey WHERE DimScenario.ScenarioName = 'Actual' GROUP BY DimOrganization.OrganizationName ORDER BY TotalAmount DESC"
  },
  {
    "input": "Top 10 product colors by internet sales",
    "query": "SELECT TOP 10 DimProduct.Color AS Color, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.Color ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 customers by total number of internet orders",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, COUNT(*) AS TotalOrders FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY TotalOrders DESC"
  },
  {
    "input": "Top 10 resellers by number of products purchased",
    "query": "SELECT TOP 10 DimReseller.ResellerName AS ResellerName, SUM(FactResellerSales.OrderQuantity) AS TotalQuantity FROM FactResellerSales INNER JOIN DimReseller ON FactResellerSales.ResellerKey = DimReseller.ResellerKey GROUP BY DimReseller.ResellerName ORDER BY TotalQuantity DESC"
  },
  {
    "input": "Top 10 product models by internet sales",
    "query": "SELECT TOP 10 DimProduct.ModelName AS ModelName, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.ModelName ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 5 territories by total inventory units movement",
    "query": "SELECT TOP 5 DimSalesTerritory.SalesTerritoryRegion AS Region, SUM(FactProductInventory.UnitsIn + FactProductInventory.UnitsOut) AS TotalUnitsMoved FROM FactProductInventory INNER JOIN DimProduct ON FactProductInventory.ProductKey = DimProduct.ProductKey INNER JOIN DimProductSubcategory ON DimProduct.ProductSubcategoryKey = DimProductSubcategory.ProductSubcategoryKey INNER JOIN DimProductCategory ON DimProductSubcategory.ProductCategoryKey = DimProductCategory.ProductCategoryKey INNER JOIN DimSalesTerritory ON DimProductCategory.ProductCategoryKey = DimSalesTerritory.SalesTerritoryKey GROUP BY DimSalesTerritory.SalesTerritoryRegion ORDER BY TotalUnitsMoved DESC"
  },
  {
    "input": "Top 5 customers with most survey responses",
    "query": "SELECT TOP 5 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, COUNT(*) AS Responses FROM FactSurveyResponse INNER JOIN DimCustomer ON FactSurveyResponse.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY Responses DESC"
  },
  {
    "input": "Top 10 cities by reseller sales",
    "query": "SELECT TOP 10 DimGeography.City AS City, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimReseller ON FactResellerSales.ResellerKey = DimReseller.ResellerKey INNER JOIN DimGeography ON DimReseller.GeographyKey = DimGeography.GeographyKey GROUP BY DimGeography.City ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 products with the highest total tax amount in internet sales",
    "query": "SELECT TOP 10 DimProduct.EnglishProductName AS ProductName, SUM(FactInternetSales.TaxAmt) AS TotalTax FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.EnglishProductName ORDER BY TotalTax DESC"
  },
  {
    "input": "Top 10 territories by total freight charges in internet sales",
    "query": "SELECT TOP 10 DimSalesTerritory.SalesTerritoryRegion AS Region, SUM(FactInternetSales.Freight) AS TotalFreight FROM FactInternetSales INNER JOIN DimSalesTerritory ON FactInternetSales.SalesTerritoryKey = DimSalesTerritory.SalesTerritoryKey GROUP BY DimSalesTerritory.SalesTerritoryRegion ORDER BY TotalFreight DESC"
  },
  {
    "input": "Top 10 employees by number of reseller sales orders handled",
    "query": "SELECT TOP 10 DimEmployee.FirstName + ' ' + DimEmployee.LastName AS EmployeeName, COUNT(*) AS TotalOrders FROM FactResellerSales INNER JOIN DimEmployee ON FactResellerSales.EmployeeKey = DimEmployee.EmployeeKey GROUP BY DimEmployee.FirstName + ' ' + DimEmployee.LastName ORDER BY TotalOrders DESC"
  },
  {
    "input": "Top 10 months by internet sales amount",
    "query": "SELECT TOP 10 DimDate.CalendarYear AS Year, DimDate.MonthNumberOfYear AS Month, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimDate ON FactInternetSales.OrderDateKey = DimDate.DateKey GROUP BY DimDate.CalendarYear, DimDate.MonthNumberOfYear ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 resellers by total annual revenue",
    "query": "SELECT TOP 10 DimReseller.ResellerName AS ResellerName, DimReseller.AnnualRevenue AS AnnualRevenue FROM DimReseller ORDER BY AnnualRevenue DESC"
  },
  {
    "input": "Top 10 products by total reseller order quantity",
    "query": "SELECT TOP 10 DimProduct.EnglishProductName AS ProductName, SUM(FactResellerSales.OrderQuantity) AS TotalQuantity FROM FactResellerSales INNER JOIN DimProduct ON FactResellerSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.EnglishProductName ORDER BY TotalQuantity DESC"
  },
  {
    "input": "Top 5 states by number of customers",
    "query": "SELECT TOP 5 DimGeography.StateProvinceName AS StateProvince, COUNT(*) AS TotalCustomers FROM DimCustomer INNER JOIN DimGeography ON DimCustomer.GeographyKey = DimGeography.GeographyKey GROUP BY DimGeography.StateProvinceName ORDER BY TotalCustomers DESC"
  },
  {
    "input": "Top 10 products with highest average unit price in internet sales",
    "query": "SELECT TOP 10 DimProduct.EnglishProductName AS ProductName, AVG(FactInternetSales.UnitPrice) AS AverageUnitPrice FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.EnglishProductName ORDER BY AverageUnitPrice DESC"
  },
  {
    "input": "Top 10 promotions generating the highest reseller sales",
    "query": "SELECT TOP 10 DimPromotion.EnglishPromotionName AS PromotionName, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimPromotion ON FactResellerSales.PromotionKey = DimPromotion.PromotionKey GROUP BY DimPromotion.EnglishPromotionName ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 dates by number of call center issues raised",
    "query": "SELECT TOP 10 DimDate.FullDateAlternateKey AS Date, SUM(FactCallCenter.IssuesRaised) AS TotalIssues FROM FactCallCenter INNER JOIN DimDate ON FactCallCenter.DateKey = DimDate.DateKey GROUP BY DimDate.FullDateAlternateKey ORDER BY TotalIssues DESC"
  },
  {
    "input": "Top 5 countries by reseller sales",
    "query": "SELECT TOP 5 DimGeography.EnglishCountryRegionName AS CountryName, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimReseller ON FactResellerSales.ResellerKey = DimReseller.ResellerKey INNER JOIN DimGeography ON DimReseller.GeographyKey = DimGeography.GeographyKey GROUP BY DimGeography.EnglishCountryRegionName ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 employees by sick leave hours",
    "query": "SELECT TOP 10 DimEmployee.FirstName + ' ' + DimEmployee.LastName AS EmployeeName, DimEmployee.SickLeaveHours AS SickLeaveHours FROM DimEmployee ORDER BY DimEmployee.SickLeaveHours DESC"
  },
  {
    "input": "Top 5 customer education levels by number of customers",
    "query": "SELECT TOP 5 EnglishEducation AS EducationLevel, COUNT(*) AS TotalCustomers FROM DimCustomer GROUP BY EnglishEducation ORDER BY TotalCustomers DESC"
  },
  {
    "input": "Top 10 product lines by internet sales amount",
    "query": "SELECT TOP 10 DimProduct.ProductLine AS ProductLine, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.ProductLine ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 5 job titles by number of employees",
    "query": "SELECT TOP 5 DimEmployee.Title AS JobTitle, COUNT(*) AS TotalEmployees FROM DimEmployee GROUP BY DimEmployee.Title ORDER BY TotalEmployees DESC"
  },
  {
    "input": "Top 10 customers by number of children",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, DimCustomer.TotalChildren AS TotalChildren FROM DimCustomer ORDER BY DimCustomer.TotalChildren DESC"
  },
  {
    "input": "Top 10 product categories by survey responses",
    "query": "SELECT TOP 10 DimProductCategory.EnglishProductCategoryName AS CategoryName, COUNT(*) AS Responses FROM FactSurveyResponse INNER JOIN DimProductCategory ON FactSurveyResponse.ProductCategoryKey = DimProductCategory.ProductCategoryKey GROUP BY DimProductCategory.EnglishProductCategoryName ORDER BY Responses DESC"
  },
  {
    "input": "Top 10 cities by internet sales",
    "query": "SELECT TOP 10 DimGeography.City AS City, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey INNER JOIN DimGeography ON DimCustomer.GeographyKey = DimGeography.GeographyKey GROUP BY DimGeography.City ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 customers by total freight paid",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, SUM(FactInternetSales.Freight) AS TotalFreight FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY TotalFreight DESC"
  },
  {
    "input": "Top 10 departments by number of employees",
    "query": "SELECT TOP 10 DimEmployee.DepartmentName AS DepartmentName, COUNT(*) AS TotalEmployees FROM DimEmployee GROUP BY DimEmployee.DepartmentName ORDER BY TotalEmployees DESC"
  },
  {
    "input": "Top 10 products by total due date delays in internet sales",
    "query": "SELECT TOP 10 DimProduct.EnglishProductName AS ProductName, SUM(DATEDIFF(day, FactInternetSales.OrderDate, FactInternetSales.DueDate)) AS TotalDelayDays FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.EnglishProductName ORDER BY TotalDelayDays DESC"
  },
  {
    "input": "Top 10 products most purchased by resellers",
    "query": "SELECT TOP 10 DimProduct.EnglishProductName AS ProductName, COUNT(*) AS PurchaseCount FROM FactResellerSales INNER JOIN DimProduct ON FactResellerSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.EnglishProductName ORDER BY PurchaseCount DESC"
  },
  {
    "input": "Top 10 sales territories by total tax amount",
    "query": "SELECT TOP 10 DimSalesTerritory.SalesTerritoryRegion AS Region, SUM(FactInternetSales.TaxAmt) AS TotalTax FROM FactInternetSales INNER JOIN DimSalesTerritory ON FactInternetSales.SalesTerritoryKey = DimSalesTerritory.SalesTerritoryKey GROUP BY DimSalesTerritory.SalesTerritoryRegion ORDER BY TotalTax DESC"
  },
  {
    "input": "Top 10 customers by total order quantity in internet sales",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, SUM(FactInternetSales.OrderQuantity) AS TotalQuantity FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY TotalQuantity DESC"
  },
  {
    "input": "Top 5 promotions by number of internet sales orders",
    "query": "SELECT TOP 5 DimPromotion.EnglishPromotionName AS PromotionName, COUNT(*) AS TotalOrders FROM FactInternetSales INNER JOIN DimPromotion ON FactInternetSales.PromotionKey = DimPromotion.PromotionKey GROUP BY DimPromotion.EnglishPromotionName ORDER BY TotalOrders DESC"
  },
  {
    "input": "Top 10 dates with highest number of automatic call center responses",
    "query": "SELECT TOP 10 DimDate.FullDateAlternateKey AS Date, SUM(FactCallCenter.AutomaticResponses) AS TotalAutoResponses FROM FactCallCenter INNER JOIN DimDate ON FactCallCenter.DateKey = DimDate.DateKey GROUP BY DimDate.FullDateAlternateKey ORDER BY TotalAutoResponses DESC"
  },
  {
    "input": "Top 10 product sizes by internet sales",
    "query": "SELECT TOP 10 DimProduct.Size AS Size, SUM(FactInternetSales.SalesAmount) AS TotalSales FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.Size ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 education levels by total yearly customer income",
    "query": "SELECT TOP 10 EnglishEducation AS EducationLevel, SUM(YearlyIncome) AS TotalIncome FROM DimCustomer GROUP BY EnglishEducation ORDER BY TotalIncome DESC"
  },
  {
    "input": "Top 5 reseller product lines by total reseller sales",
    "query": "SELECT TOP 5 DimReseller.ProductLine AS ProductLine, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimReseller ON FactResellerSales.ResellerKey = DimReseller.ResellerKey GROUP BY DimReseller.ProductLine ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 5 states by reseller sales",
    "query": "SELECT TOP 5 DimGeography.StateProvinceName AS StateProvince, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimReseller ON FactResellerSales.ResellerKey = DimReseller.ResellerKey INNER JOIN DimGeography ON DimReseller.GeographyKey = DimGeography.GeographyKey GROUP BY DimGeography.StateProvinceName ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 10 employees by total vacation hours",
    "query": "SELECT TOP 10 DimEmployee.FirstName + ' ' + DimEmployee.LastName AS EmployeeName, DimEmployee.VacationHours AS VacationHours FROM DimEmployee ORDER BY DimEmployee.VacationHours DESC"
  },
  {
    "input": "Top 10 customers by total number of purchases per year",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, COUNT(*) AS TotalPurchases FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY TotalPurchases DESC"
  },
  {
    "input": "Top 10 product categories by total reseller order quantity",
    "query": "SELECT TOP 10 DimProductCategory.EnglishProductCategoryName AS CategoryName, SUM(FactResellerSales.OrderQuantity) AS TotalQuantity FROM FactResellerSales INNER JOIN DimProduct ON FactResellerSales.ProductKey = DimProduct.ProductKey INNER JOIN DimProductSubcategory ON DimProduct.ProductSubcategoryKey = DimProductSubcategory.ProductSubcategoryKey INNER JOIN DimProductCategory ON DimProductSubcategory.ProductCategoryKey = DimProductCategory.ProductCategoryKey GROUP BY DimProductCategory.EnglishProductCategoryName ORDER BY TotalQuantity DESC"
  },
  {
    "input": "Top 10 customers by total discount amount applied",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, SUM(FactInternetSales.DiscountAmount) AS TotalDiscount FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY TotalDiscount DESC"
  },
  {
    "input": "Top 10 promotions by total reseller sales discount amount",
    "query": "SELECT TOP 10 DimPromotion.EnglishPromotionName AS PromotionName, SUM(FactResellerSales.DiscountAmount) AS TotalDiscount FROM FactResellerSales INNER JOIN DimPromotion ON FactResellerSales.PromotionKey = DimPromotion.PromotionKey GROUP BY DimPromotion.EnglishPromotionName ORDER BY TotalDiscount DESC"
  },
  {
    "input": "Top 10 customer commute distances by total customer count",
    "query": "SELECT TOP 10 CommuteDistance AS CommuteDistance, COUNT(*) AS TotalCustomers FROM DimCustomer GROUP BY CommuteDistance ORDER BY TotalCustomers DESC"
  },
  {
    "input": "Top 10 employees by total base rate salary",
    "query": "SELECT TOP 10 DimEmployee.FirstName + ' ' + DimEmployee.LastName AS EmployeeName, DimEmployee.BaseRate AS BaseRate FROM DimEmployee ORDER BY BaseRate DESC"
  },
  {
    "input": "Top 10 years by reseller total sales",
    "query": "SELECT TOP 10 DimDate.CalendarYear AS CalendarYear, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimDate ON FactResellerSales.OrderDateKey = DimDate.DateKey GROUP BY DimDate.CalendarYear ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 5 customers with highest total product cost in internet sales",
    "query": "SELECT TOP 5 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, SUM(FactInternetSales.TotalProductCost) AS TotalCost FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY TotalCost DESC"
  },
  {
    "input": "Top 10 customers by earliest order date",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, MIN(FactInternetSales.OrderDate) AS FirstOrderDate FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY FirstOrderDate"
  },
  {
    "input": "Top 10 products by total extended amount in internet sales",
    "query": "SELECT TOP 10 DimProduct.EnglishProductName AS ProductName, SUM(FactInternetSales.ExtendedAmount) AS TotalExtendedAmount FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.EnglishProductName ORDER BY TotalExtendedAmount DESC"
  },
  {
    "input": "Top 10 customers by total number of internet sales line items",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, COUNT(*) AS LineItems FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY LineItems DESC"
  },
  {
    "input": "Top 10 sales territories by total order quantity in internet sales",
    "query": "SELECT TOP 10 DimSalesTerritory.SalesTerritoryRegion AS Region, SUM(FactInternetSales.OrderQuantity) AS TotalQuantity FROM FactInternetSales INNER JOIN DimSalesTerritory ON FactInternetSales.SalesTerritoryKey = DimSalesTerritory.SalesTerritoryKey GROUP BY DimSalesTerritory.SalesTerritoryRegion ORDER BY TotalQuantity DESC"
  },
  {
    "input": "Top 10 resellers by first order year",
    "query": "SELECT TOP 10 ResellerName AS ResellerName, FirstOrderYear AS FirstOrderYear FROM DimReseller WHERE FirstOrderYear IS NOT NULL ORDER BY FirstOrderYear"
  },
  {
    "input": "Top 5 promotions by earliest start date",
    "query": "SELECT TOP 5 EnglishPromotionName AS PromotionName, StartDate AS StartDate FROM DimPromotion ORDER BY StartDate"
  },
  {
    "input": "Top 10 customers by latest purchase date",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, MAX(FactInternetSales.OrderDate) AS LatestOrderDate FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY LatestOrderDate DESC"
  },
  {
    "input": "Top 10 product subcategories by reseller sales amount",
    "query": "SELECT TOP 10 DimProductSubcategory.EnglishProductSubcategoryName AS SubcategoryName, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimProduct ON FactResellerSales.ProductKey = DimProduct.ProductKey INNER JOIN DimProductSubcategory ON DimProduct.ProductSubcategoryKey = DimProductSubcategory.ProductSubcategoryKey GROUP BY DimProductSubcategory.EnglishProductSubcategoryName ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 5 product categories by internet sales tax amount",
    "query": "SELECT TOP 5 DimProductCategory.EnglishProductCategoryName AS CategoryName, SUM(FactInternetSales.TaxAmt) AS TotalTax FROM FactInternetSales INNER JOIN DimProduct ON FactInternetSales.ProductKey = DimProduct.ProductKey INNER JOIN DimProductSubcategory ON DimProduct.ProductSubcategoryKey = DimProductSubcategory.ProductSubcategoryKey INNER JOIN DimProductCategory ON DimProductSubcategory.ProductCategoryKey = DimProductCategory.ProductCategoryKey GROUP BY DimProductCategory.EnglishProductCategoryName ORDER BY TotalTax DESC"
  },
  {
    "input": "Top 10 customers by highest number of cars owned",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, NumberCarsOwned AS NumberCarsOwned FROM DimCustomer ORDER BY NumberCarsOwned DESC"
  },
  {
    "input": "Top 10 cities by survey responses",
    "query": "SELECT TOP 10 DimGeography.City AS City, COUNT(*) AS TotalResponses FROM FactSurveyResponse INNER JOIN DimCustomer ON FactSurveyResponse.CustomerKey = DimCustomer.CustomerKey INNER JOIN DimGeography ON DimCustomer.GeographyKey = DimGeography.GeographyKey GROUP BY DimGeography.City ORDER BY TotalResponses DESC"
  },
  {
    "input": "Top 5 product colors by reseller sales",
    "query": "SELECT TOP 5 DimProduct.Color AS Color, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimProduct ON FactResellerSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.Color ORDER BY TotalSales DESC"
  },
  {
    "input": "Top 5 years by total finance amount for budget scenario",
    "query": "SELECT TOP 5 DimDate.CalendarYear AS CalendarYear, SUM(FactFinance.Amount) AS TotalAmount FROM FactFinance INNER JOIN DimDate ON FactFinance.DateKey = DimDate.DateKey INNER JOIN DimScenario ON FactFinance.ScenarioKey = DimScenario.ScenarioKey WHERE DimScenario.ScenarioName = 'Budget' GROUP BY DimDate.CalendarYear ORDER BY TotalAmount DESC"
  },
  {
    "input": "Top 10 resellers by annual sales value",
    "query": "SELECT TOP 10 ResellerName AS ResellerName, AnnualSales AS AnnualSales FROM DimReseller ORDER BY AnnualSales DESC"
  },
  {
    "input": "Top 10 currency pairs by fluctuation in end of day rate",
    "query": "SELECT TOP 10 DimCurrency.CurrencyName AS CurrencyName, MAX(FactCurrencyRate.EndOfDayRate) - MIN(FactCurrencyRate.EndOfDayRate) AS RateFluctuation FROM FactCurrencyRate INNER JOIN DimCurrency ON FactCurrencyRate.CurrencyKey = DimCurrency.CurrencyKey GROUP BY DimCurrency.CurrencyName ORDER BY RateFluctuation DESC"
  },
  {
    "input": "Top 5 product categories by total inventory units in stock",
    "query": "SELECT TOP 5 DimProductCategory.EnglishProductCategoryName AS CategoryName, SUM(FactProductInventory.UnitsBalance) AS TotalUnits FROM FactProductInventory INNER JOIN DimProduct ON FactProductInventory.ProductKey = DimProduct.ProductKey INNER JOIN DimProductSubcategory ON DimProduct.ProductSubcategoryKey = DimProductSubcategory.ProductSubcategoryKey INNER JOIN DimProductCategory ON DimProductSubcategory.ProductCategoryKey = DimProductCategory.ProductCategoryKey GROUP BY DimProductCategory.EnglishProductCategoryName ORDER BY TotalUnits DESC"
  },
  {
    "input": "Top 10 employees by number of call center shifts worked",
    "query": "SELECT TOP 10 DimEmployee.FirstName + ' ' + DimEmployee.LastName AS EmployeeName, COUNT(*) AS ShiftsWorked FROM FactCallCenter INNER JOIN DimEmployee ON FactCallCenter.LevelOneOperators = DimEmployee.EmployeeKey OR FactCallCenter.LevelTwoOperators = DimEmployee.EmployeeKey GROUP BY DimEmployee.FirstName + ' ' + DimEmployee.LastName ORDER BY ShiftsWorked DESC"
  },
  {
    "input": "Top 10 customers by total freight plus tax",
    "query": "SELECT TOP 10 DimCustomer.FirstName + ' ' + DimCustomer.LastName AS CustomerName, SUM(FactInternetSales.Freight + FactInternetSales.TaxAmt) AS TotalCharges FROM FactInternetSales INNER JOIN DimCustomer ON FactInternetSales.CustomerKey = DimCustomer.CustomerKey GROUP BY DimCustomer.FirstName + ' ' + DimCustomer.LastName ORDER BY TotalCharges DESC"
  },
  {
    "input": "Top 10 reseller regions by order quantity",
    "query": "SELECT TOP 10 DimSalesTerritory.SalesTerritoryRegion AS Region, SUM(FactResellerSales.OrderQuantity) AS TotalQuantity FROM FactResellerSales INNER JOIN DimSalesTerritory ON FactResellerSales.SalesTerritoryKey = DimSalesTerritory.SalesTerritoryKey GROUP BY DimSalesTerritory.SalesTerritoryRegion ORDER BY TotalQuantity DESC"
  },
  {
    "input": "Top 10 promotions by total number of reseller sales orders",
    "query": "SELECT TOP 10 DimPromotion.EnglishPromotionName AS PromotionName, COUNT(*) AS TotalOrders FROM FactResellerSales INNER JOIN DimPromotion ON FactResellerSales.PromotionKey = DimPromotion.PromotionKey GROUP BY DimPromotion.EnglishPromotionName ORDER BY TotalOrders DESC"
  },
  {
    "input": "Top 10 product models by total reseller sales amount",
    "query": "SELECT TOP 10 DimProduct.ModelName AS ModelName, SUM(FactResellerSales.SalesAmount) AS TotalSales FROM FactResellerSales INNER JOIN DimProduct ON FactResellerSales.ProductKey = DimProduct.ProductKey GROUP BY DimProduct.ModelName ORDER BY TotalSales DESC"
  },
  {
    "input": "Compare Internet and Reseller Sales Amount by calendar year",
    "query": "WITH InternetByDate AS (SELECT OrderDateKey,SUM(SalesAmount) AS InternetSalesAmount  FROM FactInternetSales GROUP BY OrderDateKey),ResellerByDate AS ( SELECT  OrderDateKey, SUM(SalesAmount) AS ResellerSalesAmount FROM FactResellerSales GROUP BY OrderDateKey) SELECT d.CalendarYear, SUM(ISNULL(i.InternetSalesAmount, 0)) AS InternetSalesAmount, SUM(ISNULL(r.ResellerSalesAmount, 0)) AS ResellerSalesAmount FROM DimDate d LEFT JOIN InternetByDate i  ON i.OrderDateKey  = d.DateKey LEFT JOIN ResellerByDate r  ON r.OrderDateKey  = d.DateKey GROUP BY d.CalendarYear ORDER BY d.CalendarYear"
  }
]




