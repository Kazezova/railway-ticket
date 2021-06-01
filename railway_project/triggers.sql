--###################################     1     ########################################################
--###################################     1     ########################################################
--###################################     1     ########################################################

CREATE OR ALTER TRIGGER passenger_ticket_INSERT ON passenger_ticket
AFTER INSERT
AS
BEGIN
	DECLARE @ticket_id INT = (SELECT ticket_id FROM inserted)
	UPDATE ticket SET reserve=1 WHERE ticket_id=@ticket_id
END

--###################################     2     ########################################################
--###################################     2     ########################################################
--###################################     2     ########################################################
 CREATE OR ALTER TRIGGER MAKE_NULL_DEP_TIME ON STATION_TIME
 INSTEAD OF INSERT AS
 BEGIN
	INSERT INTO STATION_TIME
	SELECT * FROM inserted ORDER BY SEQ_NUM ASC, TIME_DEP DESC
 END


--###################################     3     ########################################################
--###################################     3     ########################################################
--###################################     3     ########################################################

CREATE OR ALTER TRIGGER after_status_update ON passenger
AFTER UPDATE
AS
BEGIN
	DECLARE @OLD_status VARCHAR(255) = (SELECT status FROM deleted)
    DECLARE @NEW_status VARCHAR(255) = (SELECT status FROM inserted)
	SELECT @OLD_status, @NEW_status
	DECLARE @passenger_id INT = (SELECT passenger_id FROM deleted)
	DECLARE @cnt INT = (SELECT COUNT(*) FROM passenger_ticket pt JOIN passenger p
	ON p.passenger_id=pt.passenger_id WHERE p.passenger_id=@passenger_id)
	PRINT @cnt
	DECLARE @i INT = 0
	DECLARE @ticket_id INT

	DECLARE @price NUMERIC(9, 2)

	SET @OLD_status = ISNULL(@OLD_status, 'NULL')
	SET @NEW_status = ISNULL(@NEW_status, 'NULL')

    DECLARE @bin INT

    IF @OLD_status <> @NEW_status
	BEGIN
		IF @OLD_status = 'NULL'
			SET @bin = 1
		ELSE IF @OLD_status<>'NULL' and @NEW_status='NULL'
			SET  @bin = 0
		PRINT @bin
		WHILE (@i < @cnt)
			BEGIN
				SET @price = (SELECT price FROM passenger_ticket WHERE passenger_id=@passenger_id
								ORDER BY ticket_id
								OFFSET @i ROWS FETCH NEXT 1 ROWS ONLY)
				SET @ticket_id = (SELECT ticket_id FROM passenger_ticket WHERE passenger_id=@passenger_id
								ORDER BY ticket_id
								OFFSET @i ROWS FETCH NEXT 1 ROWS ONLY)
				PRINT @price
				UPDATE passenger_ticket SET price = dbo.FUNCTION_new_price(@NEW_status, @price, @bin)
				WHERE passenger_id = @passenger_id AND ticket_id = @ticket_id
				SET @i = @i + 1
			END
	END
END

--###################################     4     ########################################################
--###################################     4     ########################################################
--###################################     4     ########################################################

CREATE OR ALTER TRIGGER discount_INSERT ON discount
INSTEAD OF INSERT 
AS
BEGIN
	DECLARE @pas_id INT = (SELECT passenger_id FROM inserted)
	DECLARE @ex_date DATE = CONVERT(DATE, DATEADD(year, 2, GETDATE()))
	INSERT INTO discount(passenger_id, expiration_date) VALUES(@pas_id, @ex_date)
END

CREATE OR ALTER TRIGGER passenger_ticket_INSERT1 ON passenger_ticket
AFTER INSERT
AS
BEGIN
	DECLARE @id INT = (SELECT passenger_id FROM inserted)
	DECLARE @has_discount INT = (SELECT COUNT(*) FROM discount WHERE passenger_id=@id)
	IF @has_discount=1
		UPDATE discount SET cnt_trips += 1 WHERE passenger_id=@id
END

--###################################     5     ########################################################
--###################################     5     ########################################################
--###################################     5     ########################################################

CREATE OR ALTER TRIGGER return_price_for_delayed_passengers ON delay_passengers 
AFTER INSERT
AS
BEGIN
	DECLARE @cnt INT = (SELECT COUNT(*) FROM inserted)
	DECLARE @i INT = 0
	DECLARE @price NUMERIC(9,2), @ticket_id INT, @transport_company_fault VARCHAR(255)
	WHILE (@i < @cnt)
	BEGIN
		SET @price = (SELECT price FROM inserted ORDER BY ticket_id
								OFFSET @i ROWS FETCH NEXT 1 ROWS ONLY)
		SET @ticket_id = (SELECT ticket_id FROM inserted ORDER BY ticket_id
								OFFSET @i ROWS FETCH NEXT 1 ROWS ONLY)
		SET @transport_company_fault = (SELECT transport_company_fault FROM inserted ORDER BY ticket_id
								OFFSET @i ROWS FETCH NEXT 1 ROWS ONLY)
		IF @transport_company_fault = 'YES'
			BEGIN
				UPDATE delay_passengers SET compensation = price*0.5 WHERE ticket_id=@ticket_id
			END
		SET @i = @i + 1
	END
END

--###################################     6     ########################################################
--###################################     6     ########################################################
--###################################     6     ########################################################

CREATE OR ALTER TRIGGER passenger_ticket_DELETE ON passenger_ticket
AFTER DELETE
AS
BEGIN
	DECLARE @ticket_id INT = (SELECT ticket_id FROM deleted)
	UPDATE ticket SET reserve=0 WHERE ticket_id=@ticket_id
	DECLARE @id INT = (SELECT passenger_id FROM deleted)
	DECLARE @has_discount INT = (SELECT COUNT(*) FROM discount WHERE passenger_id=@id)
	IF @has_discount=1
        DECLARE @cnt INT = (SELECT cnt_trips FROM discount WHERE passenger_id=@id)
        IF @cnt > 0
		    UPDATE discount SET cnt_trips -= 1 WHERE passenger_id=@id
		ELSE
			UPDATE discount SET cnt_trips = 0 WHERE passenger_id=@id
    DECLARE @has_insured INT = (SELECT COUNT(*) FROM INSURANCE WHERE ticket_id=@ticket_id)
    IF @has_insured=1
        UPDATE ticket SET INSURED=0 WHERE ticket_id=@ticket_id
END

--###################################     7     ########################################################
--###################################     7     ########################################################
--###################################     7     ########################################################

CREATE OR ALTER TRIGGER INSURING ON INSURANCE
AFTER INSERT AS
    BEGIN
    UPDATE ticket
    SET INSURED=1
    WHERE ticket_id=(SELECT ticket_id FROM INSERTED)
END

--###################################     8     ########################################################
--###################################     8     ########################################################
--###################################     8     ########################################################
CREATE OR ALTER TRIGGER after_status_update_2
ON penalty AFTER UPDATE AS
    BEGIN
    DECLARE @NEW VARCHAR(255) = (SELECT PENALTY_STATUS FROM inserted)
    IF @NEW = 'Paid' BEGIN
    DELETE from penalty where penalty_id=(SELECT PENALTY_ID FROM deleted);
    END
END;

--###################################     9     ########################################################
--###################################     9     ########################################################
--###################################     9     ########################################################

CREATE OR ALTER TRIGGER after_review_insert ON review
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @pas_id INT = (SELECT passenger_id FROM inserted)
    DECLARE @txt VARCHAR(255) = (SELECT review_text FROM inserted)
    DECLARE @stars INT = (SELECT review_stars FROM inserted)
    DECLARE @desc VARCHAR(255) = (SELECT dbo.get_star_desc(@stars))
	INSERT INTO review(review_text, review_stars, passenger_id, review_desc) VALUES(@txt, @stars, @pas_id, @desc)
END;

--###################################     10     ########################################################
--###################################     10     ########################################################
--###################################     10     ########################################################

CREATE TRIGGER after_status_update_3
ON lost_items AFTER UPDATE AS
BEGIN
DECLARE @NEW VARCHAR(255) = (SELECT lost_item_status FROM inserted)
IF @NEW = 'Item found' BEGIN
    DELETE from lost_items where lost_item_id = (SELECT lost_item_id FROM deleted);;
END

--###################################     11     ########################################################
--###################################     11     ########################################################
--###################################     11     ########################################################
CREATE TRIGGER instead_of_update_cash ON pas_cash INSTEAD OF UPDATE
AS
BEGIN
	DECLARE @change VARCHAR(1) = (SELECT change FROM inserted)
	DECLARE @price INT = (SELECT cash FROM inserted)
	DECLARE @pas_id INT = (SELECT passenger_id FROM inserted)
	DECLARE @cash_b NUMERIC(9,2) = (SELECT dbo.cash_back(@price, @change))
	SET @price -= @cash_b
	UPDATE pas_cash SET cash = @price, change=@change WHERE passenger_id = @pas_id
END

CREATE TRIGGER after_insert ON passenger AFTER INSERT
AS
BEGIN
	DECLARE @pas_id INT = (SELECT passenger_id FROM inserted)
	INSERT INTO pas_cash(passenger_id) VALUES(@pas_id)
END