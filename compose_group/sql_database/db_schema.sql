CREATE TABLE IF NOT EXISTS chatroom (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    session_id varchar(255),
    user_id varchar(255),
    summary text NOT NULL DEFAULT '',
    long_term_plan text NOT NULL DEFAULT '',
    created_date DATE NOT NULL DEFAULT CURRENT_DATE
);
CREATE INDEX chatroom_session_index ON chatroom (session_id, user_id);

CREATE TABLE IF NOT EXISTS chatbot_messages (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id varchar(255),
    session_id varchar(255),
    bubble_id varchar(255),
    message_type varchar(32),
    body text,
    created_date DATE NOT NULL DEFAULT CURRENT_DATE
);
CREATE INDEX messages_session_index ON chatbot_messages (session_id, user_id);


CREATE TABLE IF NOT EXISTS talk_simulation (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    age INT,
    gender varchar(32),
    job TEXT,
    education TEXT,
    theme_checkboxes text[3],
    theme_reason TEXT,
    sorting_reason TEXT,
    questionnaires JSONB[] DEFAULT ARRAY[]::JSONB[],
    report TEXT,
    report_flag BOOLEAN DEFAULT TRUE,
    session_id TEXT NOT NULL,
    created_date DATE NOT NULL DEFAULT CURRENT_DATE
);
CREATE INDEX talk_simulation_index ON talk_simulation (session_id);

CREATE TABLE IF NOT EXISTS user_account (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username TEXT,
    password_hash TEXT,
    email TEXT UNIQUE,
    login_type TEXT,

    created_date DATE NOT NULL DEFAULT CURRENT_DATE
);
CREATE INDEX email_index ON user_account (email);

CREATE TYPE status_type AS ENUM ('complete', 'in_progress');
CREATE TABLE IF NOT EXISTS transcript(
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    file_name TEXT,
    session_id TEXT UNIQUE,
    user_id TEXT,
    full_text TEXT,
    status status_type NOT NULL DEFAULT 'in_progress',
    segments JSONB[] DEFAULT ARRAY[]::JSONB[],

    created_date DATE NOT NULL DEFAULT CURRENT_DATE
);
CREATE INDEX transcript_session ON transcript (session_id);
CREATE INDEX transcript_user ON transcript (user_id);

CREATE TABLE IF NOT EXISTS supervisor_report(
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    transcript_id INT,
    status status_type NOT NULL DEFAULT 'in_progress',

    case_conceptualization JSONB,
    homework_assignment JSONB,
    issue_treatment_strategies JSONB[] DEFAULT ARRAY[]::JSONB[],

    created_date DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT fk_transcript FOREIGN KEY(transcript_id) REFERENCES transcript(id)
);
