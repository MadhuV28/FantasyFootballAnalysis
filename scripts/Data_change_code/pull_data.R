library(nflfastR)
library(dplyr)
library(readr)

seasons <- 2015:2024
pbp <- purrr::map_df(seasons, function(x) {
  load_pbp(x)
})

# Example: compute some metrics
player_stats <- pbp %>%
  group_by(player_id, season) %>%
  summarize(
    air_yards = sum(air_yards, na.rm = TRUE),
    targets = sum(pass_attempt, na.rm = TRUE),
    .groups = 'drop'
  )

write_csv(player_stats, "data/real_nfl_stats.csv")
