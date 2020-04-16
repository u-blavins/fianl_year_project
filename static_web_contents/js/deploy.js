var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

var configurations = {
    0: 'BucketName',
    1: 'AccelerateConfiguration',
    2: 'AccessControl',
    3: 'AnalyticsConfiguration',
    4: 'BucketEncryption',
    5: 'CorsConfiguration',
    6: 'InventoryConfigurations'
}

var payload = {}

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";

  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline-block";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
    // This function deals with validation of the form fields
    var x, config, valid = true;
    x = document.getElementsByClassName("tab");
    config = configurations[currentTab];
    if (config == "BucketName") {
        valid = validateBucketName(x, config);
    } else if (config == "AccelerateConfiguration") {
        valid = validateAccelerateConfiguration(config);
    } else if (config == "AccessControl") {
        valid = validateAccessControl(config);
    } else if (config == "AnalyticsConfiguration") {
        valid = validateAnalyticsConfiguration(x, config);
    } else if (config == "BucketEncryption") {
        valid = validateBucketEncryption(x,config);
    } else if (config == "CorsConfiguration") {
        valid = validateCorsConfiguration(x, config);
    } else if (config == "InventoryConfigurations") {
        valid = validateInventoryConfigurations(x, config);
    }

    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
}

function validateBucketName(x, config) {
    valid = true;
    y = x[currentTab].getElementsByTagName("input");
    if (y[0].value == "" || y[0].value != y[0].value.toLowerCase()) {
        y[0].className += " invalid";
        valid = false;
    } else {
        payload[config] = y[0].value;
        console.log(payload);
    }
    return valid;
}

function validateAccelerateConfiguration(config) {
    valid = true;
    option = document.getElementById("accelerateConfig").options.selectedIndex;
    choice = document.getElementById("accelerateConfig").options[option].value;
    if (choice != "") {
        payload[config] = choice;
    } else {
        if (config in payload) {
            delete payload[config];
        }
    }
    console.log(payload);
    return valid;
}

function validateAccessControl(config) {
    valid = true;
    option = document.getElementById("accessControl").options.selectedIndex;
    choice = document.getElementById("accessControl").options[option].value;
    if (choice != "") {
        payload[config] = choice;
    } else {
        if (config in payload) {
            delete payload[config];
        }
    }
    console.log(payload);
    return valid;
}

function validateAnalyticsConfiguration(x, config) {
    var analytic = {}
    var destination = {}
    var tags = {}
    valid = true;
    enabled = document.getElementById("analyticConfig").checked;
    y = x[currentTab].getElementsByTagName("input");
    if (enabled) {
        if (y[0].value == "") {
            y[0].className += " invalid";
            valid = false;
        } else { analytic["Id"] = y[0].value; }
        if (y[1].value != "") { analytic["Prefix"] = y[1].value; }
        if (y[2].value != "") { destination["BucketAccountId"] = y[2].value; }
        if (y[3].value == "") {
            y[3].className += " invalid";
            valid = false;
        } else { destination["BucketArn"] = y[3].value; }
        if (y[4].value != "") { destination["Prefix"] = y[4].value; }
        if (y[5].value != "") { 
            tags = returnTags(y[5].value);
            if (tags != {}) { analytic["TagFilters"] = tags }
        }
        if ("Id" in analytic && "BucketArn" in destination) {
            analytic["Destination"] = destination;
            payload["AnalyticsConfiguration"] = analytic;
            console.log(payload);
        }
    }
    return valid;
}

function validateBucketEncryption(x, config) {
    valid = true;
    encryption = document.getElementById("defaultEncryption").checked;
    if (encryption) {
        y = x[currentTab].getElementsByTagName("input");
        if (y[1].value == "") {
            y[1].className += " invalid";
            valid = false;
        } else {
            payload["BucketEncryption"] = {
                SSEAlgorithm: "aws:kms",
                KMSMasterKeyID: y[1].value
            }
        }
    } else {
        payload["BucketEncryption"] = { SSEAlgorithm: "AES256" }
    }
    console.log(payload);
    return valid;
}

function validateCorsConfiguration(x, config) {
    valid = true;
    cors = {}
    enabled = document.getElementById("corsConfig").checked;
    methods = document.getElementById("allowedMethods").value;
    y = x[currentTab].getElementsByTagName("input");
    if (enabled) {
        if (y[0].value != "") { cors['Id'] = y[0].value;}
        if (y[1].value != "") {  cors['MaxAge'] = y[1].value; }
        if (y[2].value != "") { 
            var headers = returnList(y[2].value);
            if (headers.length != 0) { cors['AllowedHeaders'] = headers; }}
        if (y[3].value != "") { 
            var headers = returnList(y[3].value); 
            if (headers.length != 0) {cors['AllowedOrigins'] = headers;}
        } else {
            y[3].className += " invalid";
            valid = false;
        }
        if (y[4].value != "") { 
            var headers = returnList(y[4].value);
            if (headers.length != 0) { cors['ExposedHeaders'] = headers; }}
        if(y[5].value == "") {
            y[5].className += " invalid";
            valid=false; 
        }
        else {
            var headers = returnList(y[5].value);
            if (headers.length != 0) { cors['AllowedMethods'] = headers; }
        }
        if ("AllowedMethods" in cors && "AllowedOrigins" in cors) {
            payload["CorsConfiguration"] = [cors];
        } else {
            if ("CorsConfiguration" in payload) {
                delete payload["CorsConfiguration"];
            }
        }
    } else {
        if ("CorsConfiguration" in payload) {
            delete payload["CorsConfiguration"];
        }
    }
    console.log(payload);
    return valid;
}

function validateInventoryConfigurations(x, config) {
    valid = true;
    return valid;
}

function returnList(listString) {
    var temp = []
    strings = listString.split(",");
    for (var i = 0; i < strings.length; i++) {
        temp.push(strings[i].replace(/\s+/g, ''));
    }
    return temp;
}

function returnTags(tagStrings) {
    tagFilters = {}
    tags = tagStrings.split(",");
    for (var i = 0; i < tags.length; i++) {
        keyValue = tags[i].split("=");
        tagFilters[keyValue[0]] = keyValue[1];
    }
    return tagFilters;
}

function fixStepIndicator(n) {
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    x[n].className += " active";
}