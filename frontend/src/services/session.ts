import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { Session } from "../types/game";

export const sessionApi = createApi({
  reducerPath: "sessionApi",
  baseQuery: fetchBaseQuery({ baseUrl: process.env.API_URL }),
  endpoints: (build) => ({
    newSession: build.query<Session, void>({
      query: () => "/new",
    }),
  }),
});

export const { useNewSessionQuery } = sessionApi;
