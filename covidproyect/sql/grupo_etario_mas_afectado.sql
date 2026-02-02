SELECT
  age_group,
  AVG(monthly_rate) AS avg_rate
FROM `covid_analytics.hospitalizations_analytics`
GROUP BY age_group
ORDER BY avg_rate DESC;

