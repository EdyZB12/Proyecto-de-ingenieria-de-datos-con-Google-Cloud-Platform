SELECT
  year,
  AVG(monthly_rate) AS avg_rate
FROM `covid_analytics.hospitalizations_analytics`
GROUP BY year
ORDER BY year;
