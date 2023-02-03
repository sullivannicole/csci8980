# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC # Uni-Detect
# MAGIC 
# MAGIC This paper explore a unified method for detecting 4 different kinds of errrors:
# MAGIC 1. Uniqueness errors
# MAGIC 2. Functional dependency (FD) errors
# MAGIC 3. Outlier errors
# MAGIC 4. Spelling errors

# COMMAND ----------

# Imports
!pip install python-Levenshtein
from Levenshtein import distance as lvn_dist
import pandas as pd
import itertools
import numpy as np

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Example 1 [Spelling errors] (pp. 6-7)
# MAGIC 
# MAGIC All tables referenced below are tables in the original paper. Code is self-documenting for ease of reference.

# COMMAND ----------

tbl_2h = pd.DataFrame({'Super_Bowl': ['Super Bowl XX', 'Super Bowl XXI', 'Super Bowl XXII', 'Super Bowl XXV', 'Super Bowl XXVI', 'Super Bowl XXVII'],
                      'Season': [1985, 1986, 1987, 1990, 1991, 1992]})

# Get all combinations of Super_Bowl column, add column for min edit distance
combo_2h = pd.DataFrame(list(itertools.combinations(tbl_2h.Super_Bowl, 2)), columns = ['string1', 'string2'])
combo_2h['min_edit_distance'] = list(map(lambda x: lvn_dist(combo_2h.string1[x], combo_2h.string2[x]), range(len(combo_2h))))

combo_2h

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC What's the min MPD of the full table?

# COMMAND ----------

min(combo_2h.min_edit_distance)

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Now let's remove a row and recalculate the min MPD of the table.

# COMMAND ----------

drop_indices = np.random.choice(combo_2h.index, 1, replace=False)
combo_2h_less1 = combo_2h.drop(drop_indices)
combo_2h_less1

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC We've dropped row 13. Now let's check the new min MPD.

# COMMAND ----------

min(combo_2h_less1.min_edit_distance)

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Since the min edit distances are low overall, removing a single row doesn't result in a substantial difference in min MPD of the table. Now let's repeat the procedure, but use Table 4g this time. 

# COMMAND ----------

tbl_4g = pd.DataFrame({'Author': ['Joshua Ravetch', 'David Grae', 'Tom Garrius', 'Sibyl Gardner', 'Joy Gregory', 'Antoinette Stella'],
                      'Director': ['Steve Gomer', 'Kevin Doeling', 'Alan Myerson', 'James Hayman', 'Kevin Dowling', 'Rob Morrow']})

# Get all combinations of Super_Bowl column, add column for min edit distance
combo_4g = pd.DataFrame(list(itertools.combinations(tbl_4g.Director, 2)), columns = ['string1', 'string2'])
combo_4g['min_edit_distance'] = list(map(lambda x: lvn_dist(combo_4g.string1[x], combo_4g.string2[x]), range(len(combo_4g))))

combo_4g

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Now, using the authors' example, let's remove the anomalous Doeling-Dowling row.

# COMMAND ----------

combo_4g_less1 = combo_4g.drop(7)
combo_4g_less1

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Now let's compare the the MPD before/after the removal.

# COMMAND ----------

print(f'''Min MPD before row removal: {min(combo_4g.min_edit_distance)}
Min MPD after row removal: {min(combo_4g_less1.min_edit_distance)}''')

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC This row was the only one with a small min edit distance, so the min MPD increases greatly with its removal, indicating a possible spelling error.
