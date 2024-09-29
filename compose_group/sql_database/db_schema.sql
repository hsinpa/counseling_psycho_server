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
