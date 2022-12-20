const election_type = "president";

$("g.outer,g.txt").hover(function(e) {
    state_abbrev = $(this).attr("id").replace("_txt","");
    state = abbr_map[state_abbrev];

    $('#' + state_abbrev).addClass("hovering");

    $('#info-box').css('display','block');
    $('#info-box').find("#state_name").html(state);
    $('#info-box').find('#races').html("");

    const race_element = $("<div class='race'></div>");

    if (state == "Nebraska" && year >= 1992) {
        race_element.append("<div class='race-type'>2 winner-takes-all electoral votes +<br>3 congressional district votes.</div>");
    }
    else if (state == "Maine" && year >= 1972) {
        race_element.append("<div class='race-type'>2 winner-takes-all electoral votes +<br>2 congressional district votes.</div>");
    }
    else {
        race_element.append("<div class='race-type'>"  + data[year][state]["total_ev"] + " winner-takes-all electoral votes.</div>");
    }

    const race_data = data[year][state];

    var winner_check = "<img src='/assets/images/check.svg'></img>";
    for (const c in race_data["candidate"]) {
        race_element.append(
            "<div class='candidate'>" +
                "<div class='color " + party_class(race_data["party"][c]) + "'>" + winner_check + "</div>" +
                "<div class='name'>" + race_data["candidate"][c] + "</div>" +
                "<div class='party'>" + race_data["party"][c] + "</div>" + 
                "<div class='percent'>" + race_data["percentage"][c] + "</div>" + 
                "<div class='votes'>" + race_data["votes"][c] + "</div>" + 
            "</div>"
        );

        winner_check = "";
    }

    $('#info-box').find('#races').append(race_element);
});

function update_map_and_info() {
    var candidates = {}
    
    for (const state in data[year]) {
        const state_object =  $("#" + name_map[state] + "_shape");
        const state_data = data[year][state];

        for (const i in state_data["candidate"]) {
            const name = state_data["candidate"][i];

            if (!(name in candidates)) {
                candidates[name] = {
                    "parties": [],
                    "votes": 0,
                    "ev": 0,
                }
            }

            candidates[name]["votes"] += parseInt(state_data["votes"][i].replace(/,/g,""));
            if (!(state_data["party"][i] in candidates[name]["parties"])) {
                candidates[name]["parties"].push(state_data["party"][i]);
            }
        }

        const winner_name = state_data["candidate"][0];
        const winner_party = state_data["party"][0];
        const winner_class = party_class(winner_party);

        state_object.addClass(winner_class);
        candidates[winner_name]["ev"] += state_data["total_ev"];

        if (state=="Nebraska" && (year >= 1992 || viewing == "cart")) {
            $("#NE_CD1").addClass(winner_class);
            $("#NE_CD2").addClass(winner_class);
            $("#NE_CD3").addClass(winner_class);
        }
        else if (state=="Maine" && (year >= 1972 || viewing == "cart")) {
            $("#ME_CD1").addClass(winner_class);
            $("#ME_CD2").addClass(winner_class);        
        }

        if (state_data["split"]) {
            for (const cd in state_data["split"]) {
                const cd_object = $("#" + name_map[state] + "_" + cd);
                
                cd_object.removeClass(winner_class);
                candidates[winner_name]["ev"] -= 1;

                const cd_name = state_data["split"][cd];
                const cd_party = state_data["party"][state_data["candidate"].indexOf(cd_name)];
                cd_object.addClass(party_class(cd_party));
                candidates[cd_name]["ev"] += 1;
            }
        }
    }

    $('#votes').html("");
    $('#ev').html("");

    for (const name in candidates) {
        $('#votes').append(
            "<div>" +
            name + " - " + candidates[name]["votes"].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") +
            "</div>"
        );
        $('#ev').append(
            "<div>" +
            name + " - " + candidates[name]["ev"] + 
            "</div>"
        );

        // $('#' + party + '-ev').html(evs[party]);
        // $('#' + party + '-votes').html(votes[party].toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
    }
}