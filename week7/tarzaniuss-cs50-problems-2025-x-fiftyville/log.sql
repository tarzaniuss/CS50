-- 1. Look up details of the crime that occurred on July 28, 2024, on Humphrey Street
SELECT *
FROM crime_scene_reports
WHERE year = 2024
  AND month = 7
  AND day = 28
  AND street = 'Humphrey Street';


-- 2. Retrieve interviews from the same date to gather witness statements and potential leads
SELECT *
FROM interviews
WHERE year = 2024
  AND month = 7
  AND day = 28;


-- 3. One witness mentioned an ATM on Leggett Street — find all account numbers used there on that date
SELECT account_number
FROM atm_transactions
WHERE year = 2024
  AND month = 7
  AND day = 28
  AND atm_location = 'Leggett Street';


-- 4. Get all persons IDs from bank accounts
SELECT person_id
  FROM bank_accounts
 WHERE account_number in
 (
    SELECT account_number
      FROM atm_transactions
     WHERE year = 2024
       AND month = 7
       AND day = 28
       AND atm_location = 'Leggett Street'
 );


-- 5. Another witness mentioned seeing the thief leave the bakery in a car —
-- get all license plates that exited the bakery parking lot between 10:20 and 10:30
SELECT license_plate
FROM bakery_security_logs
WHERE year = 2024
  AND month = 7
  AND day = 28
  AND hour = 10
  AND minute BETWEEN 20 AND 30
  AND activity = 'exit';


-- 6. One witness said the thief made a short phone call after leaving —
-- get all calls on that date with duration under 60 seconds
SELECT caller, receiver
FROM phone_calls
WHERE year = 2024
  AND month = 7
  AND day = 28
  AND duration < 60;


-- 7. Authorities suspect the thief left town on the earliest flight the next day —
-- find passport numbers of passengers on the earliest flight from Fiftyville on July 29, 2024
SELECT passport_number
  FROM passengers as p
 WHERE flight_id =
 (
    SELECT f.id
      FROM flights as f
      JOIN airports as a
        ON f.origin_airport_id = a.id
      JOIN airports as a2
        ON f.destination_airport_id = a2.id
     WHERE a.city = 'Fiftyville'
       AND year = 2024
       AND month = 7
       AND day = 29
       AND hour =
    (
        SELECT MIN(hour)
          FROM flights as f
          JOIN airports as a
            ON f.origin_airport_id = a.id
          JOIN airports as a2
            ON f.destination_airport_id = a2.id
         WHERE a.city = 'Fiftyville'
           AND year = 2024
           AND month = 7
           AND day = 29
    )
 );


-- 8. Narrow down suspects by finding people who match all of the following:
-- withdrew cash from the Leggett Street ATM,
-- exited the bakery in the given time frame,
-- made a short call that day,
-- and were on the earliest flight the next day
SELECT *
  FROM people
 WHERE id in
 (
    SELECT person_id
      FROM bank_accounts
     WHERE account_number in
    (
        SELECT account_number
          FROM atm_transactions
         WHERE year = 2024
           AND month = 7
           AND day = 28
           AND atm_location = 'Leggett Street'
    )
 )
   AND license_plate in
   (
      SELECT license_plate
        FROM bakery_security_logs
       WHERE year = 2024
         AND month = 7
         AND day = 28
         AND hour = 10
         AND minute BETWEEN 15 AND 30
         AND activity = 'exit'
   )
   AND phone_number in
   (
      SELECT caller
        FROM phone_calls
       WHERE year = 2024
         AND month = 7
         AND day = 28
         AND duration < 60
   )
   AND passport_number in
   (
      SELECT passport_number
        FROM passengers as p
       WHERE flight_id =
       (
          SELECT f.id
            FROM flights as f
            JOIN airports as a
              ON f.origin_airport_id = a.id
            JOIN airports as a2
              ON f.destination_airport_id = a2.id
           WHERE a.city = 'Fiftyville'
             AND year = 2024
             AND month = 7
             AND day = 29
             AND hour =
             (
                SELECT MIN(hour)
                  FROM flights as f
                  JOIN airports as a
                    ON f.origin_airport_id = a.id
                  JOIN airports as a2
                    ON f.destination_airport_id = a2.id
                 WHERE a.city = 'Fiftyville'
                   AND year = 2024
                   AND month = 7
                   AND day = 29
              )
        )
   );


-- 9. Identify the destination city of that earliest flight
SELECT a.city as "Destination City"
  FROM flights as f
  JOIN airports as a
    ON f.destination_airport_id = a.id
 WHERE f.id =
 (
    SELECT f.id
      FROM flights as f
      JOIN airports as a
        ON f.origin_airport_id = a.id
      JOIN airports as a2
        ON f.destination_airport_id = a2.id
     WHERE a.city = 'Fiftyville'
       AND year = 2024
       AND month = 7
       AND day = 29
       AND hour =
    (
        SELECT MIN(hour)
          FROM flights as f
          JOIN airports as a
            ON f.origin_airport_id = a.id
          JOIN airports as a2
            ON f.destination_airport_id = a2.id
         WHERE a.city = 'Fiftyville'
           AND year = 2024
           AND month = 7
           AND day = 29
    )
 );


-- 10. Identify the thief’s accomplice by finding the receiver of the short call they made
SELECT name
  FROM people
 WHERE phone_number =
 (
    SELECT receiver
    FROM phone_calls
    WHERE year = 2024
    AND month = 7
    AND day = 28
    AND duration < 60
    AND caller =
    (
        SELECT phone_number
        FROM people
        WHERE id in
        (
            SELECT person_id
            FROM bank_accounts
            WHERE account_number in
            (
                SELECT account_number
                FROM atm_transactions
                WHERE year = 2024
                AND month = 7
                AND day = 28
                AND atm_location = 'Leggett Street'
            )
        )
        AND license_plate in
        (
            SELECT license_plate
                FROM bakery_security_logs
            WHERE year = 2024
                AND month = 7
                AND day = 28
                AND hour = 10
                AND minute BETWEEN 15 AND 30
                AND activity = 'exit'
        )
        AND phone_number in
        (
            SELECT caller
                FROM phone_calls
            WHERE year = 2024
                AND month = 7
                AND day = 28
                AND duration < 60
        )
        AND passport_number in
        (
            SELECT passport_number
                FROM passengers as p
            WHERE flight_id =
            (
                SELECT f.id
                    FROM flights as f
                    JOIN airports as a
                    ON f.origin_airport_id = a.id
                    JOIN airports as a2
                    ON f.destination_airport_id = a2.id
                WHERE a.city = 'Fiftyville'
                    AND year = 2024
                    AND month = 7
                    AND day = 29
                    AND hour =
                    (
                        SELECT MIN(hour)
                        FROM flights as f
                        JOIN airports as a
                            ON f.origin_airport_id = a.id
                        JOIN airports as a2
                            ON f.destination_airport_id = a2.id
                        WHERE a.city = 'Fiftyville'
                        AND year = 2024
                        AND month = 7
                        AND day = 29
                    )
                )
        )
    )
 );
