require(Modules.AI);
require(Modules.ASR);
require(Modules.Player);

let mycall = null,
    voice = Language.Premium.RU_RUSSIAN_YA_FEMALE,
    account_name = "",
    dialed_number = "",
    caller_id = "",
    flow,
    lastText = '',
    player

VoxEngine.addEventListener(AppEvents.CallAlerting, (e) => {

  mycall = e.call;
  mycall.addEventListener(CallEvents.Connected, handleCallConnected);

  account_name = e.toURI.substring(e.toURI.indexOf('.') + 1);
  account_name = account_name.substring(0, account_name.indexOf('.'));
  dialed_number = e.destination;
  caller_id = e.callerid;

  mycall.answer();

});

function startASR() {
  mycall.removeEventListener(CallEvents.PlaybackFinished, startASR);
  mycall.sendMediaTo(flow);
}


// TODO: separate into different functions,
// state machine instead of nested if statements
function handleCallConnected(e) {

  flow = AI.createDialogflow({
    lang: "en"
  });

  if (AI.Events.DialogflowResponse !== undefined)
    flow.addEventListener(AI.Events.DialogflowResponse, (event) => {
      if (event.response.queryResult !== undefined) {
        let result = event.response.queryResult

        if (result.queryText === undefined) {
          if (result.languageCode !== undefined) startASR();
          return
        }


        if (result.fulfillmentText !== undefined || result.allRequiredParamsPresent == true) {
          try {
            player = VoxEngine.createTTSPlayer(result.fulfillmentText, voice)
            player.addMarker(-500)
            player.addEventListener(PlayerEvents.PlaybackMarkerReached, startASR)
            player.sendMediaTo(mycall)
          } catch (err) {
            Logger.write('# state 5');
          }

          Logger.write(result.allRequiredParamsPresent);

          if (result.allRequiredParamsPresent == true) {
            Logger.write('# state 7')
              let msg = "";
              Net.httpRequest('https://functions.yandexcloud.net/d4erurocvcpt8dc20mfb',
                (result) => {
                  msg += " Понятно. "
                  if (result.code != 200) {
                    Logger.write("Failed");
                    Logger.write("code:  " + result.code);
                    Logger.write("data:  " + result.data);
                    Logger.write("error:  " + result.error);
                    Logger.write("headers:  " + JSON.stringify(result.headers));
                    Logger.write("raw_headers:  " + result.raw_headers);
                    Logger.write("text:  " + result.text);
                    msg += " No tables available. Sorry!";
                  } else {
                    Logger.write('OK');
                    Logger.write("data: " + result.data);
                    Logger.write("text: " + result.text);
                    Logger.write("result: " + result.result);
                    msg += " Your reservation id is " + JSON.parse(result.text)['result'] + " Thank you ";

                  }
                  Logger.write('msg' + msg)
                  player.stop()
                  player = VoxEngine.createTTSPlayer(msg, voice)
                  player.addEventListener(PlayerEvents.PlaybackFinished, () => mycall.hangup())
                  player.sendMediaTo(e.call)
                },
                Net.HttpRequestOptions({
                    method: 'POST',
                    postData: JSON.stringify({
                        'dt': result.parameters['date'],
                        'cnt': result.parameters['number'],
                    })
                  }
                )
              )

            player.stop()
            player = VoxEngine.createTTSPlayer(msg, voice)
            player.addMarker(-500)
            player.addEventListener(PlayerEvents.PlaybackMarkerReached, startASR)
            player.sendMediaTo(e.call)

          } else {

            player.stop()
            lastText = result.fulfillmentText
            player = VoxEngine.createTTSPlayer(result.fulfillmentText, voice)
              player.addMarker(-500)
              player.addEventListener(PlayerEvents.PlaybackMarkerReached, startASR)
              player.sendMediaTo(e.call)

          }
        }
      }
    })

  player = VoxEngine.createTTSPlayer("Hello. Would you like to book a table?", voice);
  player.addMarker(-500);
  player.addEventListener(PlayerEvents.PlaybackMarkerReached, startASR);
  player.sendMediaTo(e.call);

  mycall.record();
  mycall.addEventListener(CallEvents.Disconnected, (event) => {
    VoxEngine.terminate();
  })
}

