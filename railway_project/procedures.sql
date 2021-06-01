--###################################     1     ########################################################
--###################################     1     ########################################################
--###################################     1     ########################################################

CREATE OR ALTER PROCEDURE  ticket_booking_part_1 @trip_id CHAR(6), @date DATE
AS
BEGIN
    SELECT s.coach_id, s.seat_id FROM ticket t JOIN seat s ON t.seat_id = s.seat_id
    WHERE t.trip=@trip_id AND t.depature_date=@date AND t.reserve=0;
END;

CREATE OR ALTER PROCEDURE ticket_booking_part_2 @passenger_id INT, @trip_id CHAR(6), @date DATE, @seat_id INT
AS
BEGIN
    DECLARE @ticket_id INT = (SELECT ticket_id FROM ticket WHERE seat_id=@seat_id AND depature_date=@date AND trip=@trip_id)
    DECLARE @price INT = (SELECT price FROM trip WHERE trip_id=@trip_id)
    INSERT INTO passenger_ticket(passenger_id, ticket_id, price) VALUES (@passenger_id, @ticket_id, @price)
    EXEC check_discount @passenger_id=@passenger_id, @ticket_id=@ticket_id
END;

--###################################     2     ########################################################
--###################################     2     ########################################################
--###################################     2     ########################################################

 CREATE OR ALTER PROCEDURE ROUTE_OF_STATION(@FROM_STAT VARCHAR(20),@TO_STAT VARCHAR(20))
 AS BEGIN
	 DELETE FROM STATION_TIME
	 DECLARE @FROM_ID INT =(SELECT station_id FROM station WHERE station_name=@FROM_STAT),
			 @TO_ID INT = (SELECT station_id FROM station WHERE station_name=@TO_STAT)
	 DECLARE
	 @TRAIN_FROM INT = (SELECT train_id FROM schedule where station_id=@FROM_ID),
	 @TRAIN_TO INT = (SELECT train_id FROM schedule where station_id=@TO_ID),
	 @STATION VARCHAR(1000) = '',
	 @S INT = ''
	 IF @TRAIN_FROM = @TRAIN_TO
		 BEGIN
			IF @FROM_ID < @TO_ID
			 BEGIN	INSERT INTO STATION_TIME
					SELECT station_name,time_in,time_out, sequence_number
					FROM DBO.SCHED_STATION(@TRAIN_FROM,@FROM_ID,@TO_ID)
			 END
			ELSE BEGIN
				INSERT INTO STATION_TIME
				SELECT station_name,back_time_in,back_time_out, sequence_number
				FROM DBO.SCHED_STATION(@TRAIN_FROM,@TO_ID,@FROM_ID)
			 END
		 END
	 ELSE BEGIN
		SET @S=(SELECT DISTINCT B.station_id FROM
			(SELECT station_id FROM schedule WHERE train_id = @TRAIN_FROM)A
			LEFT OUTER JOIN (SELECT station_id FROM schedule WHERE train_id = @TRAIN_TO)B
			ON A.station_id=B.station_id)
		IF ISNULL(@S,'')='' BEGIN
			DECLARE @RES VARCHAR(500) = (SELECT ISNULL(DBO.CHANGE_ROUTE(@FROM_STAT,@TO_STAT),'Current route does not exist'))
			IF @RES <> 'Current route does not exist' BEGIN
				DECLARE @ST1 INT=(SELECT STATION_ID FROM STATION WHERE station_name=(SELECT ST1 FROM dbo.COMPLICATED_TAB(@TRAIN_FROM,@TRAIN_TO))),
				@ST2 INT = (SELECT STATION_ID FROM STATION WHERE station_name=(SELECT ST2 FROM DBO.COMPLICATED_TAB(@TRAIN_FROM,@TRAIN_TO)))
				IF @FROM_ID < @TO_ID BEGIN
					INSERT INTO STATION_TIME
					SELECT station_name,back_time_in,back_time_out, sequence_number FROM DBO.SCHED_STATION(@TRAIN_FROM,@ST1,@FROM_ID)
					UNION ALL
					SELECT station_name,time_in,time_out, sequence_number FROM DBO.SCHED_STATION(@TRAIN_TO,@ST2,@TO_ID);
				END
				ELSE BEGIN
					INSERT INTO STATION_TIME
					SELECT station_name,time_in,time_out, sequence_number FROM DBO.SCHED_STATION(@TRAIN_TO,@ST2,@TO_ID)
					UNION ALL
					SELECT station_name,BACK_time_in,BACK_time_out, sequence_number FROM DBO.SCHED_STATION(@TRAIN_FROM,@ST1,@FROM_ID);
				END
			END
		END
		ELSE BEGIN
			SET @STATION = (SELECT station_name FROM STATION WHERE station_id=@S)
			INSERT INTO STATION_TIME
			SELECT station_name,time_in,time_out, sequence_number FROM DBO.SCHED_STATION(@TRAIN_TO,@STATION,@TO_ID)
			UNION ALL
			SELECT station_name,BACK_time_in,BACK_time_out, sequence_number FROM DBO.SCHED_STATION(@TRAIN_FROM,@STATION,@FROM_ID);
		END
	 END
 END


--###################################     3     ########################################################
--###################################     3     ########################################################
--###################################     3     ########################################################

CREATE OR ALTER PROCEDURE PROCEDURE3_50_percent_discount @passengerid INT, @new_status VARCHAR(255)
AS
BEGIN
    UPDATE passenger SET status = @new_status WHERE passenger_id = @passengerid;
END

--###################################     4     ########################################################
--###################################     4     ########################################################
--###################################     4     ########################################################
CREATE OR ALTER PROCEDURE check_discount @passenger_id INT, @ticket_id INT
AS
BEGIN
	DECLARE @temp TABLE(d_id INT, p_id INT, cnt_trips INT, ex_date DATE)
	INSERT INTO @temp SELECT * FROM discount WHERE passenger_id=@passenger_id
	IF(NOT EXISTS(SELECT 1 FROM @temp))
		BEGIN
		  RAISERROR('У пассажира нет дисконтной карты.', 16, 1)
		END
	ELSE
		BEGIN
		IF CONVERT(DATE, GETDATE())>(SELECT ex_date FROM @temp)
			RAISERROR('К сожалению, срок действия дисконтной карты истек.', 16, 1)
		ELSE
			BEGIN
				DECLARE @persent INT = (SELECT cnt_trips FROM @temp)
				SET @persent = dbo.down_persent(@persent)
				UPDATE passenger_ticket SET price -= price*@persent/100, discount_persentage=@persent
					   WHERE passenger_id=@passenger_id AND ticket_id=@ticket_id
				SELECT 'Пассажир имеет '+ CONVERT(CHAR(3), @persent) +'% скидку.'
			END
		END
END


--###################################     5     ########################################################
--###################################     5     ########################################################
--###################################     5     ########################################################

CREATE PROCEDURE PROCEDURE5_train_delay(@station_1 int, @station_2 int, @train_id int,
				@train_delay_time time, @transport_company_fault VARCHAR(255), @direction VARCHAR(255),
				@reason VARCHAR(255))
AS
BEGIN
    INSERT INTO train_delay VALUES(@station_1, @station_2, @train_id,
				@train_delay_time, @transport_company_fault, @direction, @reason);
END

CREATE OR ALTER PROCEDURE PROCEDURE5_train_schedule
AS
BEGIN
    SELECT SS.station_name, S.train_id,
		dbo.Function5_Change_time(S.station_id, TD.station_1, TD.station_2, TD.direction,S.time_in, 1,TD.train_delay_time) as time_in,
        dbo.Function5_Change_time(S.station_id, TD.station_1, TD.station_2, TD.direction,S.time_out, 2,TD.train_delay_time) as time_out,
        dbo.Function5_Change_time(S.station_id, TD.station_1, TD.station_2, TD.direction,S.back_time_in, 3,TD.train_delay_time) as back_time_in,
        dbo.Function5_Change_time(S.station_id, TD.station_1, TD.station_2, TD.direction,S.back_time_out, 4,TD.train_delay_time) as back_time_out,
		dbo.Function5_in_time(S.station_id, TD.station_1, TD.station_2, TD.direction) as schedule_in_time, TD.train_delay_time, TD.reason
		FROM
		schedule S
		join train T
		ON S.train_id=T.train_id
		join
		station SS
		on S.station_id = SS.station_id
		left join train_delay TD
		on T.train_id = TD.train_id;
END

CREATE PROCEDURE report_delay_passengers AS
BEGIN
	INSERT INTO delay_passengers(train_name, delay_time, transport_company_fault, first_name,
	last_name, identification, ticket_id, price)
	SELECT tr.train_name, td.train_delay_time, td.transport_company_fault,
	p.first_name, p.last_name, p.identification, t.ticket_id, pt.price FROM
	passenger p JOIN passenger_ticket pt ON p.passenger_id=pt.passenger_id
	JOIN ticket t ON pt.ticket_id=t.ticket_id
	JOIN seat s ON t.seat_id=s.seat_id
	JOIN coach c ON c.coach_id=s.coach_id
	JOIN train tr ON c.train_id=tr.train_id
	JOIN train_delay td ON td.train_id=tr.train_id;
END

--###################################     6     ########################################################
--###################################     6     ########################################################
--###################################     6     ########################################################

CREATE OR ALTER PROCEDURE ticket_return @ticket_id INT
AS
BEGIN
	IF NOT EXISTS (SELECT * FROM passenger_ticket WHERE ticket_id=@ticket_id)
		RAISERROR('Пассажир не покупал такой билет.', 16, 1)
	ELSE
		DECLARE @ticket_price NUMERIC(9,2) = (SELECT price FROM passenger_ticket
			WHERE ticket_id=@ticket_id)
		DECLARE @date DATE = (SELECT depature_date FROM ticket WHERE ticket_id=@ticket_id)
		DECLARE @return_price NUMERIC(9,2) = dbo.ticket_return_price(@ticket_price, @date)
		SELECT 'Пассажиру возвращается сумма билета со штрафом ' + CONVERT(VARCHAR(100), @return_price) + ' тг.'
		DECLARE @passenger_id INT = (SELECT passenger_id FROM passenger_ticket WHERE ticket_id=@ticket_id)
		DELETE FROM passenger_ticket WHERE ticket_id=@ticket_id
END

CREATE PROCEDURE report_of_train @train_id INT AS
BEGIN
SELECT p.first_name, p.last_name, p.identification, t.depature_date,
			 s.station_name AS from_station, s1.station_name AS to_station,
			 tra.train_name, c.coach_id/100%100 AS coach, st.seat_id%100 AS seat FROM
	passenger_ticket pt
	JOIN
	passenger p
	ON pt.passenger_id = p.passenger_id
	JOIN ticket t
	ON pt.ticket_id=t.ticket_id
	JOIN trip tr
	ON tr.trip_id=t.trip
	JOIN station s
	ON tr.from_station = s.station_id
	JOIN station s1
	ON tr.to_station = s1.station_id
	JOIN seat st
	ON st.seat_id=t.seat_id
	JOIN coach c
	ON st.coach_id=c.coach_id
	JOIN train tra
	ON tra.train_id=c.train_id
	WHERE tra.train_id=@train_id
END;

CREATE OR ALTER PROCEDURE report_of_passenger @passenger_id INT AS
BEGIN
SELECT p.first_name, p.last_name, p.identification, p.status, t.depature_date,
			 s.station_name AS from_station, s1.station_name AS to_station, t.ticket_id,
			 tra.train_name, c.coach_id/100%100 AS coach, st.seat_id%100 AS seat, pt.price AS price FROM
	passenger_ticket pt
	JOIN
	passenger p
	ON pt.passenger_id = p.passenger_id
	JOIN ticket t
	ON pt.ticket_id=t.ticket_id
	JOIN trip tr
	ON tr.trip_id=t.trip
	JOIN station s
	ON tr.from_station = s.station_id
	JOIN station s1
	ON tr.to_station = s1.station_id
	JOIN seat st
	ON st.seat_id=t.seat_id
	JOIN coach c
	ON st.coach_id=c.coach_id
	JOIN train tra
	ON tra.train_id=c.train_id
	WHERE p.passenger_id=@passenger_id;
END;

--###################################     7     ########################################################
--###################################     7     ########################################################
--###################################     7     ########################################################
CREATE OR ALTER PROCEDURE BUY_INSURANCE (@TICKET_ID INT) AS
BEGIN
    DECLARE @PRICE INT = (SELECT ROUND(price*0.2,0,1) FROM trip WHERE trip_id=(SELECT trip FROM ticket where ticket_id=@TICKET_ID)),
    @check bit = (SELECT DBO.CHECK_PRIVILEGE(@TICKET_ID))
    INSERT INTO INSURANCE(TICKET_ID)
    VALUES (@TICKET_ID)
END

--###################################     8     ########################################################
--###################################     8     ########################################################
--###################################     8     ########################################################

CREATE OR ALTER PROCEDURE PROCEDURE7_penalty(@passenger_id int, @penalty_description VARCHAR(255),
@penalty_price int, @penalty_status VARCHAR(255)) AS
BEGIN
INSERT INTO penalty VALUES( @passenger_id, @penalty_description, DBO.FUNCTION_penalty_price(@penalty_description, @penalty_price), @penalty_status);
END;

CREATE OR ALTER PROCEDURE PROCEDURE7_penalty_paid(@penalty_idd int, @penalty_statuss VARCHAR(255))
AS BEGIN
    UPDATE penalty set penalty_status = @penalty_statuss WHERE penalty_id = @penalty_idd;
END;

--###################################     9     ########################################################
--###################################     9     ########################################################
--###################################     9     ########################################################
CREATE OR ALTER PROCEDURE PROCEDURE9_review(@review_text VARCHAR(255), @review_stars int, @passenger_id int) AS
BEGIN
    INSERT INTO review(review_text, review_stars, passenger_id) VALUES( @review_text, @review_stars, @passenger_id);
END;

--###################################     10     ########################################################
--###################################     10     ########################################################
--###################################     10     ########################################################
CREATE PROCEDURE PROCEDURE8_lost_items( @lost_item_name VARCHAR(255),
                            @lost_item_description VARCHAR(255), @lost_item_status VARCHAR(255),
                            @lost_item_weight int, @lost_item_repayment int) AS
BEGIN
    INSERT INTO lost_items VALUES(@lost_item_name,@lost_item_description,@lost_item_status,@lost_item_weight, dbo.FUNCTION_lost_item_repaiment(@lost_item_weight,@lost_item_repayment));
END;

CREATE PROCEDURE PROCEDURE8_lost_items_status(@id int, @status VARCHAR(255))
AS BEGIN
    UPDATE lost_items set lost_item_status = @status WHERE lost_item_id = @id;
END;

--###################################     11     ########################################################
--###################################     11     ########################################################
--###################################     11     ########################################################

CREATE OR ALTER PROCEDURE purchase(@pas_id int, @change VARCHAR(1), @price INT)
AS BEGIN
	UPDATE pas_cash SET cash = @price, change=@change WHERE passenger_id = @pas_id
END;
