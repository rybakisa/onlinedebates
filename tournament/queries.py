TAB_QUERY = """
SELECT T.name as team_name,
  SUM(R.score) as sum,
  r1_results.score as r1,
  r2_results.score as r2,
  r3_results.score as r3,
  r4_results.score as r4,
  r5_results.score as r5

FROM tournament_team as T
  LEFT JOIN tournament_result as R ON T.id = R.team_id

  LEFT JOIN
    (SELECT results.team_id as team_id, results.score as score
      FROM tournament_round as round
        LEFT JOIN tournament_room as room ON round.id = room.round_id
        LEFT JOIN tournament_result as results ON room.id = results.room_id
      WHERE round.number = 1) as r1_results ON r1_results.team_id = T.id

  LEFT JOIN
    (SELECT results.team_id as team_id, results.score as score
      FROM tournament_round as round
        LEFT JOIN tournament_room as room ON round.id = room.round_id
        LEFT JOIN tournament_result as results ON room.id = results.room_id
      WHERE round.number = 2) as r2_results ON r2_results.team_id = T.id

  LEFT JOIN
    (SELECT results.team_id as team_id, results.score as score
      FROM tournament_round as round
        LEFT JOIN tournament_room as room ON round.id = room.round_id
        LEFT JOIN tournament_result as results ON room.id = results.room_id
      WHERE round.number = 3) as r3_results ON r3_results.team_id = T.id

  LEFT JOIN
    (SELECT results.team_id as team_id, results.score as score
      FROM tournament_round as round
        LEFT JOIN tournament_room as room ON round.id = room.round_id
        LEFT JOIN tournament_result as results ON room.id = results.room_id
      WHERE round.number = 4) as r4_results ON r4_results.team_id = T.id

  LEFT JOIN
    (SELECT results.team_id as team_id, results.score as score
      FROM tournament_round as round
        LEFT JOIN tournament_room as room ON round.id = room.round_id
        LEFT JOIN tournament_result as results ON room.id = results.room_id
      WHERE round.number = 5) as r5_results ON r5_results.team_id = T.id

GROUP BY team_name
ORDER BY sum DESC;
"""