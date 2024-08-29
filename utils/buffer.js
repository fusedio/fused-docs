// Used under Apache 2.0 license
// https://github.com/whitphx/stlite/blob/c66239e8699bd85a8ee6b52b3d5a433ca89caf2c/packages/sharing-common/src/buffer.ts#L1
/**
 * Ad-hoc value that works at least on Chromium: 105.0.5195.102（Official Build） （arm64）.
 * Decrease this if `RangeError: Maximum call stack size exceeded` is reported.
 */
const DEFAULT_APPLY_MAX = 2 ** 16;

export function u8aToBase64(buf, applyMax) {
  // If `buf` is too long, `String.fromCharCode.apply(null, buf)`
  // throws `RangeError: Maximum call stack size exceeded`,
  // so we split the buffer into chunks and process them one by one.
  let str = "";
  const nChunks = Math.ceil(buf.length / (applyMax ?? DEFAULT_APPLY_MAX));
  for (let i = 0; i < nChunks; ++i) {
    const offset = DEFAULT_APPLY_MAX * i;
    const chunk = buf.slice(offset, offset + DEFAULT_APPLY_MAX);
    str += String.fromCharCode.apply(null, chunk);
  }

  return btoa(str);
}
