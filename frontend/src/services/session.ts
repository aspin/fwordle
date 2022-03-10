import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { Session } from "../types/game";

const apiPath = "http://localhost:9000";

export const sessionApi = createApi({
  reducerPath: "sessionApi",
  baseQuery: fetchBaseQuery({ baseUrl: apiPath }),
  endpoints: (build) => ({
    newSession: build.query<Session, void>({
      query: () => "/new",
    }),
  }),
});

export const { useNewSessionQuery } = sessionApi;
