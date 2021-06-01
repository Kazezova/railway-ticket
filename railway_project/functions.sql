--###################################     1     ########################################################
--###################################     1     ########################################################
--###################################     1     ########################################################
CREATE FUNCTION booking_status (@status INT) RETURNS VARCHAR(255) AS
	BEGIN
	DECLARE @text VARCHAR(255)
	IF @status=1
		SET @text = 'Booking was successful!'
	ELSE
		SET @text = 'All seats have been booked, your reservation is canceled.'
	RETURN @text
END

--###################################     2     ########################################################
--###################################     2     ########################################################
--###################################     2     ########################################################


   --1 FUNCTION
 CREATE OR ALTER FUNCTION SCHED_STATION(@TRAIN INT,@START_ID INT,@END_ID INT)
 RETURNS TABLE AS
 RETURN
	 SELECT S.station_name, SC.* FROM schedule SC JOIN station S ON SC.station_id=S.station_id
	 WHERE SC.train_id=@TRAIN AND SC.station_id BETWEEN @START_ID AND @END_ID

 --2 FUNCTION
 CREATE OR ALTER FUNCTION CHANGE_ROUTE (@FROM VARCHAR(100),@TO VARCHAR(100))
 RETURNS VARCHAR(1000)
 AS BEGIN
	DECLARE @STR VARCHAR(1000),
	@TRAIN_FROM INT = (SELECT train_id FROM schedule SC JOIN station S ON SC.station_id=S.station_id WHERE S.station_name=@FROM),
	@TRAIN_TO INT = (SELECT train_id FROM schedule SC JOIN station S ON SC.station_id=S.station_id WHERE S.station_name=@TO),
	@FIRST_ROUTE VARCHAR(500)='',@SECOND_ROUTE VARCHAR(500)=''

	SELECT @FIRST_ROUTE = DBO.DIRECT_ROUTE(@TRAIN_FROM,@FROM,ST1), @SECOND_ROUTE = DBO.DIRECT_ROUTE(@TRAIN_TO,ST2,@TO)
	from (SELECT A.station_name ST1,B.station_name ST2 FROM (SELECT station_name,SC.*,station_location
	FROM schedule SC JOIN station S ON SC.station_id=S.station_id)A
	JOIN (SELECT station_name,SC.*,station_location
	FROM schedule SC JOIN station S ON SC.station_id=S.station_id)B
	ON A.station_location=B.station_location
	WHERE A.train_id=@TRAIN_FROM AND B.train_id=@TRAIN_TO)Z
	SET @STR = @FIRST_ROUTE + ' &  ' + @SECOND_ROUTE
	RETURN @STR
 END

 --3 FFUNCTION
 CREATE OR ALTER FUNCTION DIRECT_ROUTE (@TRAIN INT,@FROM_STAT VARCHAR(100),@TO_STAT VARCHAR(100))
 RETURNS VARCHAR(1000)
 AS BEGIN
	DECLARE @STR VARCHAR(1000),
	@FROM_STAT_ID INT = (SELECT station_id FROM station WHERE station_name=@FROM_STAT),
	@TO_STAT_ID INT = (SELECT station_id FROM station WHERE station_name=@TO_STAT)
	IF @FROM_STAT_ID<@TO_STAT_ID
		SET @STR=
		(SELECT station_name+'  ' FROM schedule SC
		JOIN station S ON SC.station_id=S.station_id
		WHERE SC.station_id BETWEEN @FROM_STAT_ID AND @TO_STAT_ID AND train_id=@TRAIN
		FOR XML PATH(''))
	ELSE
		SET @STR=
		(SELECT station_name+'  ' FROM schedule SC
		JOIN station S ON SC.station_id=S.station_id
		WHERE SC.station_id BETWEEN @TO_STAT_ID AND @FROM_STAT_ID AND train_id=@TRAIN
		ORDER BY SC.sequence_number DESC
		FOR XML PATH(''))
	RETURN @STR
 END
-- 4 FUNCTION
 CREATE OR ALTER FUNCTION COMPLICATED_TAB(@TRAIN_FROM INT,@TRAIN_TO INT)
 RETURNS TABLE AS RETURN
 SELECT A.station_name AS ST1,B.station_name AS ST2 FROM (SELECT station_name,SC.*,station_location
	FROM schedule SC JOIN station S ON SC.station_id=S.station_id)A
	JOIN (SELECT station_name,SC.*,station_location
	FROM schedule SC JOIN station S ON SC.station_id=S.station_id)B
	ON A.station_location=B.station_location
	WHERE A.train_id=@TRAIN_FROM AND B.train_id=@TRAIN_TO

--5 FUNCTION
 CREATE OR ALTER FUNCTION TOTAL_TIME(@FROM_STAT VARCHAR(20),@TO_STAT VARCHAR(20))
 RETURNS time(0) AS
 BEGIN
	DECLARE @TIME_DEPART TIME(0) = (SELECT TIME_DEP FROM STATION_TIME WHERE STATION_NAME=@FROM_STAT),
	@TIME_ARRIV TIME(0) = (SELECT TIME_ARR FROM STATION_TIME WHERE STATION_NAME=@TO_STAT),
	@TIME TIME(0)
	SET @TIME = DATEADD(MINUTE,DATEDIFF(MINUTE,@TIME_DEPART,@TIME_ARRIV),0)
	RETURN @TIME
 END
  --6 FUNCTION
 CREATE OR ALTER FUNCTION PROCEDURE2_RES(@FROM_STAT VARCHAR(20),@TO_STAT VARCHAR(20))
 RETURNS VARCHAR(500) AS
 BEGIN
	 DECLARE @FROM_ID INT =(SELECT station_id FROM station WHERE station_name=@FROM_STAT),
			 @TO_ID INT = (SELECT station_id FROM station WHERE station_name=@TO_STAT)
	 DECLARE
		@TRAIN_FROM INT = (SELECT train_id FROM schedule where station_id=@FROM_ID),
		@TRAIN_TO INT = (SELECT train_id FROM schedule where station_id=@TO_ID),
		@RES VARCHAR(500) = ''
	IF @TRAIN_FROM = @TRAIN_TO BEGIN
		SET @RES=(SELECT DBO.DIRECT_ROUTE(@TRAIN_FROM,@FROM_STAT,@TO_STAT))
	END
	ELSE BEGIN
		SET @RES = (SELECT ISNULL(DBO.CHANGE_ROUTE(@FROM_STAT,@TO_STAT),
		'Current route does not exist'))
	END
	RETURN @RES
 END


--###################################     3     ########################################################
--###################################     3     ########################################################
--###################################     3     ########################################################

CREATE OR ALTER FUNCTION FUNCTION_new_price(@status VARCHAR(255), @price INT, @discount INT) 
RETURNS INT AS
BEGIN
	SET @status = LOWER(@status)
	IF @status = 'pensioner' and @discount = 1 
		SET @price = (@price/100)*50
	ELSE IF @status = 'student' and @discount = 1 
		SET @price = (@price/100)*50
	ELSE IF @status = 'NULL' and @discount = 0 
		SET @price = (@price/50)*100
	ELSE
		SET @price = @price
	RETURN @price
END

--###################################     4     ########################################################
--###################################     4     ########################################################
--###################################     4     ########################################################

CREATE FUNCTION down_persent (@persent INT) RETURNS INT AS
BEGIN
	IF @persent >= 100
		SET @persent = 100
	RETURN @persent
END

--###################################     5     ########################################################
--###################################     5     ########################################################
--###################################     5     ########################################################

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

CREATE OR ALTER FUNCTION Function5_Change_time(@station_id int, @station_1 int, @station_2 int, 
@direction VARCHAR(255), @Timee time, @HH int, @train_delay_time time) RETURNS time AS
BEGIN
	declare @station int;
    declare @Situation int;
    declare @TIMETIME time;
	IF @station_1 = @station_2 
		BEGIN
			SET @station = @station_1;
			SET @Situation = 0;
		END
	ELSE
		BEGIN
			SET @station = @station_2;
			SET @Situation = 1;
		END
/*# 1 #*/    
    IF @station = @station_id and @direction = 'FORWARD' 
		BEGIN
			IF @Situation = 0 
				BEGIN
					IF @HH = 1
						BEGIN
							Set @TIMETIME = @Timee;
						END
					ELSE
						BEGIN
							Set @TIMETIME = DATEADD(second,DATEDIFF(second,0,CONVERT(TIME(0),@train_delay_time)),CONVERT(TIME(0),@Timee));
						END
				END
			ELSE IF @Situation = 1 
				BEGIN
					Set @TIMETIME = DATEADD(second,DATEDIFF(second,0,CONVERT(TIME(0),@train_delay_time)),CONVERT(TIME(0),@Timee));
				END
		END
/*# 2 #*/  
	ELSE IF @station = @station_id and @direction = 'BACKWARD'
		BEGIN
			IF @Situation = 0 
				BEGIN
					IF @HH = 1 or @HH = 2 
						Set @TIMETIME = @Timee;
					ELSE IF @HH = 3 
						Set @TIMETIME = @Timee;
					ELSE
						Set @TIMETIME = DATEADD(second,DATEDIFF(second,0,CONVERT(TIME(0),@train_delay_time)),CONVERT(TIME(0),@Timee));
				END
			ELSE IF @Situation = 1
				BEGIN
					IF @HH = 1 or @HH = 2 
						Set @TIMETIME = @Timee;
					ELSE
						Set @TIMETIME = DATEADD(second,DATEDIFF(second,0,CONVERT(TIME(0),@train_delay_time)),CONVERT(TIME(0),@Timee));
				END
		END
/*# 3 #*/  
	ELSE IF @station > @station_id and @direction = 'FORWARD'
		BEGIN
			IF @HH = 1 or @HH = 2 
				Set @TIMETIME = @Timee;
			ELSE
				Set @TIMETIME = DATEADD(second,DATEDIFF(second,0,CONVERT(TIME(0),@train_delay_time)),CONVERT(TIME(0),@Timee));
		END
/*# 4 #*/ 
	ELSE IF @station < @station_id and @direction = 'FORWARD'
		Set @TIMETIME = DATEADD(second,DATEDIFF(second,0,CONVERT(TIME(0),@train_delay_time)),CONVERT(TIME(0),@Timee));
/*# 5 #*/        
	ELSE IF @station < @station_id and @direction = 'BACKWARD'
        Set @TIMETIME = @Timee;
/*# 6 #*/  
	ELSE IF @station > @station_id and @direction = 'BACKWARD'
		BEGIN
			IF @HH = 1 or @HH = 2 
				Set @TIMETIME = @Timee;
			ELSE
				Set @TIMETIME = DATEADD(second,DATEDIFF(second,0,CONVERT(TIME(0),@train_delay_time)),CONVERT(TIME(0),@Timee));
		END
/*# 7 #*/  
	ELSE
		Set @TIMETIME = @Timee;
	RETURN @TIMETIME;
END;

CREATE FUNCTION Function5_in_time(@station_id int, @station_1 int, @station_2 int, @direction VARCHAR(255)) 
RETURNS VARCHAR(255) AS
BEGIN
	declare @station int;
    declare @TEXT VARCHAR(255);
	IF @station_1 = @station_2 
		SET @station = @station_1;
	ELSE
		SET @station = @station_2;
    IF @station = @station_id and @direction = 'FORWARD' 
		SET @TEXT = 'FORWARD direction not in time and BACKWARD not in time.';
	ELSE IF @station = @station_id and @direction = 'BACKWARD' 
		SET @TEXT = 'FORWARD direction in time and BACKWARD not in time.';
	ELSE IF @station > @station_id and @direction = 'FORWARD' 
		SET @TEXT = 'FORWARD direction in time and BACKWARD not in time.';
	ELSE IF @station < @station_id and @direction = 'FORWARD' 
		SET @TEXT = 'FORWARD direction not in time and BACKWARD not in time.';
	ELSE IF @station < @station_id and @direction = 'BACKWARD' 
		SET @TEXT = 'FORWARD direction in time and BACKWARD in time.';
	ELSE IF @station > @station_id and @direction = 'BACKWARD' 
		SET @TEXT = 'FORWARD direction in time and BACKWARD not in time.';
	ELSE
		SET @TEXT = 'FORWARD direction in time and BACKWARD in time.';
	RETURN @TEXT;
END;

--###################################     6     ########################################################
--###################################     6     ########################################################
--###################################     6     ########################################################

CREATE FUNCTION ticket_return_price (@price NUMERIC(9,2), @date DATE) RETURNS NUMERIC(9,2) AS
BEGIN
	DECLARE @return NUMERIC(9,2)
	DECLARE @diff INT = DATEDIFF(day, GETDATE(), @date)
	IF @diff > 30
		SET @return = @price
	ELSE IF @diff > 20
		SET @return = @price*0.9
	ELSE IF @diff > 10
		SET @return = @price*0.7
	ELSE IF @diff > 7
		SET @return = @price*0.5
	ELSE IF @diff > 3
		SET @return = @price*0.2
	ELSE
		SET @return = 0
	RETURN @return
END

CREATE FUNCTION get_trip_info() RETURNS TABLE AS
RETURN
SELECT t.trip_id, s1.station_name AS from_station, s2.station_name AS to_station, t.price FROM trip t
JOIN station s1 ON t.from_station=s1.station_id
JOIN station s2 ON t.to_station=s2.station_id

--###################################     7     ########################################################
--###################################     7     ########################################################
--###################################     7     ########################################################


CREATE OR ALTER FUNCTION CHECK_PRIVILEGE(@TICKET_ID INT)
RETURNS BIT AS
    BEGIN
    DECLARE @STATUS VARCHAR(15) =
    (SELECT [STATUS] FROM PASSENGER WHERE PASSENGER_ID = (SELECT passenger_id FROM passenger_ticket WHERE ticket_id=@TICKET_ID))
    RETURN IIF(@STATUS IN ('student','pensioner'),1,0)
END

CREATE OR ALTER FUNCTION INSURANCE_RES(@TICKET_ID INT)
RETURNS VARCHAR(200) AS
BEGIN
    DECLARE @PRICE INT = (SELECT ROUND(price*0.2,0,1) FROM trip WHERE trip_id=(SELECT trip FROM ticket where ticket_id=@TICKET_ID)),
    @check bit = (SELECT DBO.CHECK_PRIVILEGE(@TICKET_ID))
    RETURN
    IIF( @check=1,
    'Так как у вас есть лготность, вы получите страховку бесплатно ',
    CONCAT('Страховка будет стоить 20% от полной стоимости билета: ', @PRICE, 'тг.'))
END

--###################################     8     ########################################################
--###################################     8     ########################################################
--###################################     8     ########################################################

CREATE OR ALTER FUNCTION FUNCTION_penalty_price(@penalty_description VARCHAR(255), @penalty_price int)
RETURNS int AS
    BEGIN
    IF @penalty_description = 'Smoked in the wrong place' BEGIN
    Set @penalty_price = 10000 END
    ELSE IF @penalty_description = 'Fight on the train with other passengers' BEGIN
    Set @penalty_price = 25000 END
    ELSE IF @penalty_description = 'Got drunk on the train' BEGIN
    Set @penalty_price = 20000 END
    ELSE BEGIN
    Set @penalty_price = 5000;
    END
    RETURN @penalty_price;
END;

--###################################     9     ########################################################
--###################################     9     ########################################################
--###################################     9     ########################################################
CREATE OR ALTER FUNCTION get_star_desc(@stars INT) RETURNS VARCHAR(255)
AS
BEGIN
    DECLARE @txt VARCHAR(255)
    IF @stars=1 OR @stars=2
        SET @txt = 'Негативный'
    ELSE IF @stars=3
        SET @txt = 'Нейтральный'
    ELSE
        SET @txt = 'Позитивный'
    RETURN @txt
END

--###################################     10     ########################################################
--###################################     10     ########################################################
--###################################     10     ########################################################

CREATE FUNCTION FUNCTION_lost_item_repaiment(@lost_item_weigh int,@lost_item_repayment int)
RETURNS int AS
BEGIN
    Set @lost_item_repayment = @lost_item_weigh * 1000
    RETURN @lost_item_repayment;
END;


--###################################     11     ########################################################
--###################################     11     ########################################################
--###################################     11     ########################################################
CREATE OR ALTER FUNCTION cash_back(@price INT, @change VARCHAR(1)) RETURNS NUMERIC(9, 2)
AS
BEGIN
    DECLARE @cash_b NUMERIC(9, 2) = 0
		IF @change = '-'
		BEGIN
			IF @price > 3000
				SET @cash_b = @price*0.02
		END
	RETURN @cash_b
END

CREATE OR ALTER FUNCTION valid_cash(@price INT, @cash NUMERIC(9, 2)) RETURNS BIT
AS
BEGIN
	DECLARE @check BIT
    IF @price > @cash
		SET @check = 0
	ELSE
		SET @check = 1
	RETURN @check
END