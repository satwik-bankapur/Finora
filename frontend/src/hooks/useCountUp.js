import { useEffect, useRef, useState } from 'react';

export function useCountUp(targetValue, duration = 1200) {
  const [value, setValue] = useState(0);
  const startTime = useRef(null);

  useEffect(() => {
    const target = Number(targetValue) || 0;
    const step = (timestamp) => {
      if (!startTime.current) startTime.current = timestamp;
      const progress = Math.min((timestamp - startTime.current) / duration, 1);
      const next = Math.floor(progress * target);
      setValue(next);
      if (progress < 1) requestAnimationFrame(step);
    };
    setValue(0);
    startTime.current = null;
    requestAnimationFrame(step);
    return () => {
      startTime.current = null;
    };
  }, [targetValue, duration]);

  return value;
}
