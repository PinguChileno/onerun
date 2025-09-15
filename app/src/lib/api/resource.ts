import type { Client } from "./client";

export abstract class APIResource {
  protected _client: Client;

  constructor(client: Client) {
    this._client = client;
  }
}
