import Tooltip from './Tooltip';
import styles from '../../styles/InputField.module.css';

function InputField({
  label,
  name,
  type = 'text',
  value,
  onChange,
  placeholder = ' ',
  prefix,
  tooltip,
  helper,
  error,
  ...rest
}) {
  return (
    <div className={styles.field}>
      <div className={`${styles.inputWrap} ${prefix ? styles.withPrefix : ''}`}>
        {prefix && <span className={styles.prefix}>{prefix}</span>}
        <input
          id={name}
          name={name}
          className={`${styles.input} ${error ? styles.error : ''}`}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          {...rest}
        />
        <label htmlFor={name} className={styles.label}>
          {label}
          {tooltip && <Tooltip content={tooltip} className={styles.tooltipIcon} />}
        </label>
      </div>
      {error ? <div className={styles.errorText}>{error}</div> : null}
      {helper && !error ? <div className={styles.helper}>{helper}</div> : null}
    </div>
  );
}

export default InputField;
