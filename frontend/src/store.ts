import { configureStore } from "@reduxjs/toolkit";
import gameReducer from "./features/game/gameSlice";
import selectorReducer from "./features/selector/selectorSlice";
import { sessionApi } from "./services/session";

export const store = configureStore({
  reducer: {
    game: gameReducer,
    selector: selectorReducer,
    [sessionApi.reducerPath]: sessionApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(sessionApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;

export type AppDispatch = typeof store.dispatch;
