CREATE DATABASE ImageStore;
USE DATABASE ImageStore;
CREATE TABLE image_table(
   image_key VARCHAR(255) NOT NULL,
   image_tag VARCHAR(255) NOT NULL,
   PRIMARY KEY (image_key)
);
CREATE TABLE cache_properties(
    param_key INT NOT NULL AUTO_INCREMENT,
    epoch_date INT NOT NULL,
    max_capacity INT NOT NULL,
    replacement_method VARCHAR(255) NOT NULL,
    PRIMARY KEY (param_key)
);

