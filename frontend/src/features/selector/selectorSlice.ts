import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface SelectorSlice {
  sessionId: string;
  username: string;
}

const initialState: SelectorSlice = {
  sessionId: "",
  username: "",
};

export const selectorSlice = createSlice({
  name: "selector",
  initialState,
  reducers: {
    setSessionId: (state, action: PayloadAction<string>) => {
      state.sessionId = action.payload;
    },
    setUsername: (state, action: PayloadAction<string>) => {
      state.username = action.payload;
    },
  },
});

export const { setSessionId, setUsername } = selectorSlice.actions;

export default selectorSlice.reducer;
