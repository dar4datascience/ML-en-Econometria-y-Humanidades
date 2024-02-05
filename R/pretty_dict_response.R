library(dplyr)

#source_python("Python scripts/simple_batch_classifcation.py")

ml_sources_df <- py$ml_sources_df 

wrong_entries <- ml_sources_df |> 
  filter(year_of_publication == 0) |> 
  count()


ml_sources_df |> 
  readr::write_csv("data/ml_sources_df.csv")
