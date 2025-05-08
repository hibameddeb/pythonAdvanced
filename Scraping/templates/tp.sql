Create or replace trigger EtatAbsenceTrigger before insert or update on ABSENCE for each row
begin
    dbms_output.put_line('Ancienne valeur :' ||:old.ETATABSENCE ||' Nouvelle valeur :'|| :new.ETATABSENCE);
    if (not (:new.ETATABSENCE in ('A','P'))) then
        raise_application_error(-20000,'valeur de l''etat d''absence est errone');
    end if;
end;


insert into  isett.absence (CIN , CODEMAT ,DATEABSENCE ,SEANCEABSENCE, ETATABSENCE)
values ('00000001','INFO4','01-01-2021',5,'P')



update isett.absence set etatabsence='7'

--afficher les noms des triggers cree
SELECT trigger_name from user_triggers;


set  LINESIZE 100
col text format A80
elect distinct name ,type from user_source;




--creer un etable nomme AUDITTrigger table qui contient les champs suivant dateexcution, evenement(insert delete update on ...) ,user_audit
--ecrire un declancher qui permet d'effectuee l'audit de chaque evene^ment de chaque utilisateur dans chaque table etudiant absence  matiere inscription
--ajouter les declenchers qui permetent de modifier le solde en cas de chargement ou de commuication


CREATE TABLE AUDITTRIGGER (
    dateexecution   DATE DEFAULT SYSDATE,   
    evenement       VARCHAR2(20),            
    user_audit      VARCHAR2(30)             
);

CREATE OR REPLACE TRIGGER audit_etudiant_trigger
AFTER INSERT OR UPDATE OR DELETE ON etudiant
FOR EACH ROW
DECLARE
    v_evenement VARCHAR2(30);
BEGIN
    IF INSERTING THEN
        v_evenement := 'INSERT on etudiant';
    ELSIF UPDATING THEN
        v_evenement := 'UPDATE on etudiant';
    ELSIF DELETING THEN
        v_evenement := 'DELETE on etudiant';
    END IF;

    INSERT INTO AUDITTRIGGER (dateexecution, evenement, user_audit)
    VALUES (
        SYSDATE,
        v_evenement,
        USER
    );
END;
/



CREATE OR REPLACE TRIGGER audit_absence_trigger
AFTER INSERT OR UPDATE OR DELETE ON absence
FOR EACH ROW
DECLARE
    v_evenement VARCHAR2(30);
BEGIN
    IF INSERTING THEN
        v_evenement := 'INSERT on absence';
    ELSIF UPDATING THEN
        v_evenement := 'UPDATE on absence';
    ELSIF DELETING THEN
        v_evenement := 'DELETE on absence';
    END IF;

    INSERT INTO AUDITTRIGGER (dateexecution, evenement, user_audit)
    VALUES (
        SYSDATE,
        v_evenement,
        USER
    );
END;
/


CREATE OR REPLACE TRIGGER audit_matiere_trigger
AFTER INSERT OR UPDATE OR DELETE ON matiere
FOR EACH ROW
DECLARE
    v_evenement VARCHAR2(30);
BEGIN
    IF INSERTING THEN
        v_evenement := 'INSERT on matiere';
    ELSIF UPDATING THEN
        v_evenement := 'UPDATE on matiere';
    ELSIF DELETING THEN
        v_evenement := 'DELETE on matiere';
    END IF;

    INSERT INTO AUDITTRIGGER (dateexecution, evenement, user_audit)
    VALUES (
        SYSDATE,
        v_evenement,
        USER
    );
END;
/


CREATE OR REPLACE TRIGGER audit_inscription_trigger
AFTER INSERT OR UPDATE OR DELETE ON inscription
FOR EACH ROW
DECLARE
    v_evenement VARCHAR2(30);
BEGIN
    IF INSERTING THEN
        v_evenement := 'INSERT on inscription';
    ELSIF UPDATING THEN
        v_evenement := 'UPDATE on inscription';
    ELSIF DELETING THEN
        v_evenement := 'DELETE on inscription';
    END IF;

    INSERT INTO AUDITTRIGGER (dateexecution, evenement, user_audit)
    VALUES (
        SYSDATE,
        v_evenement,
        USER
    );
END;
/







CREATE OR REPLACE TRIGGER trg_update_solde_chargement
AFTER INSERT ON chargement
FOR EACH ROW
BEGIN
    UPDATE abonne
    SET solde = solde + :NEW.MONTANTCHARGEMENT
    WHERE numtel = :NEW.numtel;
END;
/


CREATE OR REPLACE TRIGGER trg_update_solde_comm
AFTER INSERT ON communication
FOR EACH ROW
DECLARE
    duree_minutes NUMBER;
    tarif_minute NUMBER := 0.05; 
    montant NUMBER;
BEGIN
    duree_minutes := (
        (EXTRACT(DAY FROM :NEW.H_COMMUNICATION_FIN - :NEW.H_COMMUNICATION_DEBUT) * 24 * 60) +
        (EXTRACT(HOUR FROM :NEW.H_COMMUNICATION_FIN - :NEW.H_COMMUNICATION_DEBUT) * 60) +
        (EXTRACT(MINUTE FROM :NEW.H_COMMUNICATION_FIN - :NEW.H_COMMUNICATION_DEBUT)) +
        (EXTRACT(SECOND FROM :NEW.H_COMMUNICATION_FIN - :NEW.H_COMMUNICATION_DEBUT) / 60)
    );

    montant := ROUND(duree_minutes * tarif_minute, 2);

    UPDATE abonne
    SET solde = solde - montant
    WHERE numtel = :NEW.numtel;
END;
/
