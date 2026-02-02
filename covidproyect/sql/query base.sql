CREATE OR REPLACE TABLE `covid_analytics.hospitalizations_analytics`
PARTITION BY year_month
AS
SELECT
  CAST(year AS INT64) AS year,
  CAST(month_int AS INT64) AS month,
  DATE(CAST(year AS INT64), CAST(month_int AS INT64), 1) AS year_month,
  range_age_clean AS age_group,
  pandemic_phase,
  seansonality AS season,
  CAST(MonthlyRate AS FLOAT64) AS monthly_rate
FROM `covid_analytics.hospitalizations_clean`
WHERE MonthlyRate IS NOT NULL;
