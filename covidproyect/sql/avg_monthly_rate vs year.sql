SELECT
  year,
  AVG(MonthlyRate) AS avg_monthly_rate
FROM `covid_analytics.hospitalizations_clean`
GROUP BY year
ORDER BY year;
