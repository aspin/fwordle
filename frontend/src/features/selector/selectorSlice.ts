import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface SelectorSlice {
  sessionId: string;
}

const initialState: SelectorSlice = {
  sessionId: "",
};

export const selectorSlice = createSlice({
  name: "selector",
  initialState,
  reducers: {
    setSessionId: (state, action: PayloadAction<string>) => {
      state.sessionId = action.payload;
    },
  },
});

export const { setSessionId } = selectorSlice.actions;

export default selectorSlice.reducer;
