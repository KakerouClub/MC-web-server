import { Component, signal } from '@angular/core';
import { HubConnection, HubConnectionBuilder, HubConnectionState } from '@microsoft/signalr';
import { environment } from '../../../environments/environment.development';

@Component({
  selector: 'app-panel',
  imports: [],
  templateUrl: './panel.html',
  styleUrl: './panel.css',
})
export class Panel {
  hubUrl = environment.hubsUrl;
  hubConnection?: HubConnection;
  outputThread = signal<string>('');

  createConnection() {
    this.hubConnection = new HubConnectionBuilder()
      .withUrl(this.hubUrl + "panel")
      .withAutomaticReconnect()
      .build();

    this.hubConnection.start().catch(error => console.log(error));

    this.hubConnection.on("ReceiveOutput", output => {
      this.outputThread.set(output);
    })
  }

  stopConnection() {
    if (this.hubConnection?.state === HubConnectionState.Connected)
      this.hubConnection.stop().catch(error => console.log(error));
  }
}
