var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

var configurations = {
    0: 'BucketName',
    1: 'AccelerateConfiguration',
    2: 'AccessControl',
    3: 'AnalyticsConfiguration',
    4: 'BucketEncryption',
    5: 'CorsConfiguration',
    6: 'InventoryConfigurations',
    7: 'LifecycleConfiguration',
    8: 'LoggingConfiguration',
    9: 'MetricsConfigurations',
    10: 'NotificationConfiguration',
    11: 'ObjectLockConfiguration',
    12: 'PublicAccessBlockConfiguration',
    13: 'ReplicationConfiguration',
    14: 'Tags',
    15: 'VersioningConfiguration',
    16: 'WebsiteConfiguration'
}

var payload = {}
var env = {}

function showTab(n) {
    var x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline-block";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").style.display = "none";
        document.getElementById("validateBtn").style.display = "none";
        document.getElementById("deployBtn").style.display = "none";
        document.getElementById("downloadBtn").style.display = "inline-block";
    }
    else if (n == (x.length - 2)) {
        document.getElementById("nextBtn").style.display = "none";
        document.getElementById("downloadBtn").style.display = "none";
        document.getElementById("validateBtn").style.display = "inline-block";
        document.getElementById("deployBtn").style.display = "inline-block";
    }  else {
        document.getElementById("nextBtn").innerHTML = "Next";
        document.getElementById("nextBtn").style.display = "inline-block";
        document.getElementById("validateBtn").style.display = "none";
        document.getElementById("deployBtn").style.display = "none";
        document.getElementById("downloadBtn").style.display = "none";
    }
    fixStepIndicator(n)
}

function validate(n) {
    var x = document.getElementsByClassName("tab");
    if (Object.keys(payload).length != 0) {
        var body = {governance: 'ENABLED', option: 'VALIDATION',
            payload: payload, env: env}

        fetch('https://qc6lo72n44.execute-api.eu-west-2.amazonaws.com/beta/provisioner', {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        })
        .then(r => r.json())
        .then(d => {
            if (d.executionArn !== '') {
                getExectutionStatus(
                    'https://qc6lo72n44.execute-api.eu-west-2.amazonaws.com/beta/execution',
                    JSON.stringify(d))
            }
        })
        .catch(err => { console.log(err) });
        nextPrev(n)
    } else {
        M.toast({html: 'Bucket payload is empty'});
        return false;
    }
}

function deploy(n) {
    var x = document.getElementsByClassName("tab");
    if (Object.keys(payload).length != 0) {
        var body = {governance: 'ENABLED', option: 'DEPLOY',
            payload: payload, env: env}

        fetch('https://qc6lo72n44.execute-api.eu-west-2.amazonaws.com/beta/provisioner', {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        })
        .then(r => r.json())
        .then(d => {
            if (d.executionArn !== '') {
                getExectutionStatus(
                    'https://qc6lo72n44.execute-api.eu-west-2.amazonaws.com/beta/execution',
                    JSON.stringify(d))
            }
        })
        .catch(err => { console.log(err) });
        nextPrev(n)
    } else {
        M.toast({html: 'Bucket payload is empty'});
        return false;
    }
    showTab(currentTab);
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
    // validation or deployment 
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
    } else if (config == "LifecycleConfiguration") {
        valid = validateLifecycleConfiguration(x, config);
    } else if (config == "LoggingConfiguration") {
        valid = validateLoggingConfiguration(x, config);
    } else if (config == "MetricsConfigurations") {
        valid = validateMetricsConfiguration(x, config);
    } else if (config == "NotificationConfiguration") {
        valid = validateNotificationConfiguration(x, config);
    } else if (config == "ObjectLockConfiguration") {
        valid = validateObjectLockConfiguration(x, config);
    } else if (config == "PublicAccessBlockConfiguration") {
        valid = validatePublicAccessBlockConfiguration(x, config);
    } else if (config == "ReplicationConfiguration") {
        valid = validateReplicationConfiguration(x, config);
    } else if (config == "Tags") {
        valid = validateTags(x, config);
    } else if (config == "VersioningConfiguration") {
        valid = validateVersioningConfiguration(config);
    } else if (config == "WebsiteConfiguration") {
        valid = validateWebsiteConfiguration(x, config);
        document.getElementById('payloadText').value = JSON.stringify(payload, undefined, 3);
        M.textareaAutoResize($('#payloadText'));
    }
    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid;
}

function validateBucketName(x, config) {
    valid = true;
    y = x[currentTab].getElementsByTagName("input");
    if (y[0].value == "" || y[0].value != y[0].value.toLowerCase()) {
        if (y[0].value != y[0].value.toLowerCase()) {
            M.toast({html: 'Bucket name must be lowercase'});
        }
        y[0].className += " invalid";
        valid = false;
    } else {
        payload[config] = y[0].value;
        console.log(payload);
    }
    if (y[1].value != "Choose Region") { 
        y[1].className = "input-field col s12"; 
        if (y[1].value == "eu-west-1 (Ireland)") { env["region"] = "eu-west-1"; }
        if (y[1].value == "eu-west-2 (London)") { env["region"] = "eu-west-2"; }
        console.log(env);
    }
    else { y[1].className += " invalid"; valid = false;}
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
        if (y[1].value != "") {  cors['MaxAge'] = parseInt(y[1].value); }
        if (y[2].value != "") { var headers = returnList(y[2].value);
            if (headers.length != 0) { cors['AllowedHeaders'] = headers; }}
        if (y[3].value != "") { 
            var headers = returnList(y[3].value); 
            if (headers.length != 0) {cors['AllowedOrigins'] = headers;}
        } else { y[3].className += " invalid"; valid = false; }
        if (y[4].value != "") { 
            var headers = returnList(y[4].value);
            if (headers.length != 0) { cors['ExposedHeaders'] = headers; }}
        if(y[5].value == "") { y[5].className += " invalid"; valid=false; }
        else {
            y[5].className = "select-dropdown dropdown-trigger";
            var headers = returnList(y[5].value);
            if (headers.length != 0) { cors['AllowedMethods'] = headers; }
        }
        if ("AllowedMethods" in cors && "AllowedOrigins" in cors) {
            payload["CorsConfiguration"] = [cors];
        } else {
            if ("CorsConfiguration" in payload) { delete payload["CorsConfiguration"]; }
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
    inventory = {}
    destination = {}
    enabled = document.getElementById('inventoryConfig').checked;
    y = x[currentTab].getElementsByTagName("input");
    if (enabled) {
        console.log(y[5].className);
        if (y[0].value != "") { inventory["Id"] = y[0].value; }
        else { y[0].className += " invalid"; valid = false; }
        if (y[1].value != "") { inventory["Prefix"] = y[1].value; }
        if (y[2].value != "") { destination["BucketAccountId"] = y[2].value; }
        if (y[3].value != "") { destination["BucketArn"] = y[3].value; }
        else { y[3].className += " invalid"; valid = false; }
        if (y[4].value != "") { destination["Prefix"] = y[4].value; }
        if (y[5].value != "Choose Inventory Status") { 
            y[5].className = "select-dropdown dropdown-trigger";
            if (y[5].value == "Enabled") { inventory["Enabled"] = true; }
            else { inventory["Enabled"] = false; }}
        else { y[5].className += " invalid"; valid = false; }
        if (y[6].value != "Choose Object Versions") { 
            y[6].className = "select-dropdown dropdown-trigger";
            inventory["IncludedObjectVersions"] = y[6].value; }
        else { y[6].className += " invalid"; valid = false; }
        if (y[7].value != "Choose Scheduled Frequency") { 
            y[7].className = "select-dropdown dropdown-trigger";
            inventory["ScheduleFrequency"] = y[7].value; }
        else { y[7].className += " invalid"; valid = false; }
        if (y[8].value != "") {
            var headers = returnList(y[8].value); 
            if (headers.length != 0) { inventory['OptionalFields'] = headers;}
        }
        if ("Id" in inventory && "Enabled" in inventory &&
            "IncludedObjectVersions" in inventory && "ScheduleFrequency" in inventory &&
            "BucketArn" in destination) {
                inventory['Destination'] = destination;
                payload["InventoryConfigurations"] = [inventory];
        }
    } else {
        if ("InventoryConfigurations" in payload) { delete payload["InventoryConfigurations"]; }
    }
    console.log(payload);
    return valid;
}

function validateLifecycleConfiguration(x, config) {
    valid = true;
    lifecycle = {}
    transition = {}
    enabled = document.getElementById('lifecycleConfig').checked;
    y = x[currentTab].getElementsByTagName("input");
    if (enabled) {
        if (y[0].value != "") { lifecycle["Id"] = y[0].value;}
        if (y[1].value != "") { lifecycle["Prefix"] = y[1].value;}
        if (y[2].value != "") { lifecycle["AbortIncompleteMultipartUpload"] = parseInt(y[2].value);}
        if (y[3].value != "") { lifecycle["ExpirationDate"] = y[3].value;}
        if (y[4].value != "") { lifecycle["ExpirationInDays"] = parseInt(y[4].value);}
        if (y[5].value != "") { lifecycle["NoncurrentVersionExpirationInDays"] = parseInt(y[5].value);}
        if (y[6].value != "Storage Class" && y[7].value != "") {
            lifecycle["NoncurrentVersionTransitions"] = 
            [{StorageClass: y[6].value, TransitionInDays: y[7].value}]}
        if (y[8].value != "Storage Class") {
            if (y[9].value != "") {
                transition = {StorageClass: y[8].value, TransitionDate: y[9].value};
            } else if (y[10].value != "") {
                transition = {StorageClass: y[8].value, TransitionInDay: y[10].value};
            }
            if ("TransitionDate" in transition || "TransitionInDays" in transition) {
                lifecycle["Transitions"] = [transition]}
        }
        if (y[11].value != "") { lifecycle["TagFilters"] = returnTags(y[11].value);}
        if (y[12].value != "Choose Lifecycle Status") { 
            y[12].className = "select-dropdown dropdown-trigger";
            lifecycle["Status"] = y[12].value; } 
        else {
            y[12].className += " invalid";
            valid = false;
        }
        if ("Status" in lifecycle) {
            if ("AbortIncompleteMultipartUpload" in lifecycle || "ExpirationDate" in lifecycle || "ExpirationInDays" in lifecycle ||
            "NoncurrentVersionExpirationInDays" in lifecycle || "NoncurrentVersionTransitions" in lifecycle || "Transitions" in lifecycle ) {
                payload["LifecycleConfiguration"] = [lifecycle];
            } else {
                M.toast({html: 'Choose a lifecycle configuration'});
                valid = false;
            }
        }
    } else {
        if ("LifecycleConfiguration" in payload) { delete payload["LifecycleConfiguration"];}}
    console.log(payload);
    return valid;
}

function validateLoggingConfiguration(x, config) {
    valid = true;
    logging = {}
    y = x[currentTab].getElementsByTagName("input");
    if (y[0].value != "") {logging["DestinationBucketName"] = y[0].value}
    if (y[1].value != "") {logging["LogFilePrefix"] = y[1].value}
    if ("DestinationBucketName" in logging || "LogFilePrefix" in logging) {
        payload[config] = logging;
    }
    console.log(payload);
    return valid;
}

function validateMetricsConfiguration(x, config) {
    valid = true;
    metric = {}
    enable = document.getElementById("metricsConfig").checked;
    y = x[currentTab].getElementsByTagName("input");
    if (enable) {
        if (y[0].value != "") { metric["Id"] = y[0].value; }
        else { y[0].className += " invalid"; valid = false; }
        if (y[1].value != "") { metric["Prefix"] = y[1].value; }
        if (y[2].value != "") { metric["TagFilters"] = returnTags(y[2].value); }
        if ("Id" in metric) { payload[config] = [metric]; }
    } else { if (config in payload) { delete payload[config]; }}
    console.log(payload);
    return valid;
}

function validateNotificationConfiguration(x, config) {
    valid = true;
    notif = "";
    notif_config = {}
    enable = document.getElementById("notificationConfig").checked;
    y = x[currentTab].getElementsByTagName("input");
    if (enable) {
        if (y[0].value != "Choose Notification") {
            y[0].className = "select-dropdown dropdown-trigger";
            if (y[0].value == "Lambda") { notif = "LambdaConfigurations"; }
            if (y[0].value == "Queue") { notif = "QueueConfigurations"; }
            if (y[0].value == "Topic") { notif = "TopicConfigurations"; }
        } else { y[0].className += " invalid"; valid=false; }
        if (y[1].value != "" && y[0].value != "Choose Notification") { 
            switch (y[0].value) {
                case "Lambda":
                    notif_config["Function"] = y[1].value;
                    break;
                case "Queue":
                    notif_config["Queue"] = y[1].value;
                    break;
                case "Topic":
                    notif_config["Topic"] = y[1].value;
                    break;
            }
        }
        else { y[1].className += " invalid"; valid = false; }
        if (y[2].value != "") { notif_config["Event"] = y[2].value; }
        else { y[2].className += " invalid"; valid = false; }
        if (y[3].value != "Filter Name" && y[4].value != "") {
            notif_config = { Name: y[3].value, Value: y[4].value }}
        if (notif != "" && "Event" in notif_config) {
            switch (notif) {
                case "LambdaConfigurations":
                    payload[config] = { "LambdaConfigurations" : [notif_config] };
                    break;
                case "QueueConfigurations":
                    payload[config] = { "QueueConfigurations" : [notif_config] };
                    break;
                case "TopicConfigurations":
                    payload[config] = { "TopicConfigurations" : [notif_config] };
                    break;
            }
        }
    } else { if (config in payload) { delete payload[config]; }}
    console.log(payload);
    return valid;
}

function validateObjectLockConfiguration(x, config) {
    valid = true;
    time = "";
    object_lock = {}
    y = x[currentTab].getElementsByTagName("input");
    enable = document.getElementById("objectLockConfig").checked;
    if (enable) {
        object_lock["ObjectLockEnabled"] = "Enabled";
        if (y[0].value != "Choose Mode") { object_lock["Mode"] = y[0].value;}
        if (y[1].value != "Choose Day/Year") { time = y[1].value;}
        if (time != "" && y[2].value != "") {object_lock[time] = parseInt(y[2].value);}
        payload["ObjectLockConfiguration"] = object_lock;
    } else { if (config in payload) {delete payload[config];}}
    console.log(payload);
    return valid;
}

function validatePublicAccessBlockConfiguration(x, config) {
    valid = true;
    blockPublicAcls = document.getElementById('blockPublicAcls').checked;
    blockPublicPolicy = document.getElementById('blockPublicPolicy').checked;
    ignorePublicAcls = document.getElementById('ignorePublicAcls').checked;
    restrictPublicBuckets = document.getElementById('restrictPublicBuckets').checked;
    payload["PublicAccessBlock"] = {
        BlockPublicAcls: blockPublicAcls,
        BlockPublicPolicy: blockPublicPolicy,
        IgnorePublicAcls: ignorePublicAcls,
        RestrictPublicBuckets: restrictPublicBuckets
    }
    console.log(payload);
    return valid;
}

function validateReplicationConfiguration(x, config) {
    valid = true;
    replication = {}
    rule = {}
    destination = {}
    enable = document.getElementById("replicationConfig").checked;
    kmsEnable = document.getElementById("sseKmsEnabled").checked;
    y = x[currentTab].getElementsByTagName("input");
    if (enable) {
        if (y[0].value != "") { replication["Role"] = y[0].value; }
        else { y[0].className += " invalid"; valid = false; }
        if (y[1].value != "") { rule["Id"] = y[1].value; }
        if (y[2].value == "") { rule["Prefix"] = "~"; }
        else { rule["Prefix"] = "~"; }
        if (kmsEnable) { rule["SseKmsEncryptionEnabled"] = "Enabled"; }
        else { rule["SseKmsEncryptionEnabled"] = "Disabled"; }
        if (y[4].value != "") { destination["Owner"] = y[4].value; }
        if ("Owner" in destination) {
            if (y[5].value != "") { destination["Account"] = y[5].value; }
            else { y[5].className += " invalid"; valid = false; }
        }
        if (y[6].value != "") { destination["Bucket"] = y[6].value; }
        else { y[6].className += " invalid"; valid = false; }
        if (y[7].value != "") { destination["ReplicaKmsKeyID"] = y[7].value; }
        if (y[8].value != "Storage Class") { destination["StorageClass"] = y[8].value; }
        if ("Bucket" in destination) { rule["Destination"] = destination; }
        if ("Destination" in rule && "Role" in replication) {
            replication["Rules"] = [rule];
            payload["ReplicationConfiguration"] = replication;
        } 
    } else { if (config in payload) {delete payload[config];}}
    console.log(payload);
    return valid;
}

function validateTags(x, config) {
    valid = true;
    var tags = {}
    var add_tags = {}
    y = x[currentTab].getElementsByTagName("input");
    if (y[0].value != "") {tags["Owner"] = y[0].value; }
    else {y[0].className += " invalid"; valid = false;} 
    if (y[1].value != "") {tags["Info"] = y[1].value; }
    else {y[1].className += " invalid"; valid = false; }
    if (y[2].value != "") { add_tags = returnTags(y[2].value); }
    if ("Owner" in tags && "Info" in tags) {
        add_key = Object.keys(add_tags);
        if (add_key.length > 0) { 
            for (var i = 0; i < add_key.length; i++) { 
                tags[add_key[i]] = add_tags[add_key[i]];}}
        payload[config] = tags;
    }
    console.log(payload);
    return valid;
}

function validateVersioningConfiguration(config) {
    valid = true;
    enable = document.getElementById("versioningConfig").checked;
    if (enable) { payload[config] = "Enabled"; }
    else { payload[config] = "Suspended"; }
    console.log(payload);
    return valid;
}

function validateWebsiteConfiguration(x, config) {
    valid = true;
    var website = {}
    var redirect_request = {}
    var redirect_rules = {}
    var redirect_condition = {}
    var routing_rules = {}
    enable = document.getElementById("websiteConfig").checked;
    y = x[currentTab].getElementsByTagName("input");
    if (enable) {
        if (y[0].value != "") { website["IndexDocument"] = y[0].value; }
        if (y[1].value != "") { website["ErrorDocument"] = y[1]. value; }
        if (y[2].value != "") { redirect_request["Hostname"] = y[2].value; }
        if (y[3].value != "Choose Protocol") { redirect["Protocol"] = y[2].value; }
        if (y[4].value != "") { redirect_rules["HostName"] = y[4].value; }
        if (y[5].value != "") { redirect_rules["HttpRedirectCode"] = y[5].value; }
        if (y[6].value != "Choose Protocol") { redirect_rules["Protocol"] = y[6].value; }
        if (y[7].value != "") { redirect_rules["ReplaceKeyPrefixWith"] = y[7].value; }
        if (y[8].value != "") { redirect_rules["ReplaceKeyWith"] = y[8].value; }
        if (y[9].value != "") { redirect_condition["HttpErrorCodeReturnsEquals"] = y[9].value; }
        if (y[10].value != "") { redirect_condition["KeyPrefixEquals"] = y[10].value; }
        if ("Hostname" in redirect_request) {
            payload[config] = { "RedirectAllRequestsTo": redirect_request }
        } else
        {
            if (Object.keys(redirect_rules).length > 0) {
                routing_rules["RedirectRules"] = redirect_rules;
            }
            if (Object.keys(redirect_condition).length > 0) {
                routing_rules["RoutingRuleCondition"] = redirect_condition;
            }
            if ("RedirectRules" in routing_rules) {
                website["RoutingRules"] = [routing_rules];
            }
            payload[config] = website;
        }
    } else { if (config in payload) {delete payload[config]; }}
    console.log(payload);
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

function getExectutionStatus(url, arn) {
    fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {'Content-Type': 'application/json'},
        body: arn
    })
    .then(resp => resp.json())
    .then(d => { 
        if (d.status == 'RUNNING') {
            getExectutionStatus(url, arn);
        } else {
            var data = JSON.parse(d.output);
            document.getElementById('cfTemplate').value = JSON.stringify(data['Template'], undefined, 3);
            M.textareaAutoResize($('#cfTemplate'));
        }
     })
    .catch(err => { console.log(err) })
}

function downloadJson() {
    var data = JSON.parse(document.getElementById('cfTemplate').value);
    var bucketName = data["Resources"]["Bucket"]["Properties"]["BucketName"];
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data, undefined, 3));
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href",     dataStr);
    downloadAnchorNode.setAttribute("download", bucketName + ".json");
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}